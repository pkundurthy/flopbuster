
import numpy as num
from flopbuster.readdb import getInfluenceHistory, getPartHistory, getReleaseDateMovie
from flopbuster.misc import getYear
from readdb import dbConnect

def getResponseTraining(year='2006-12-31'):
    """   """

    cursor = dbConnect()
    statement1 = 'select title,released,ifnull(totalgross,0),ifnull(budget,0)'
    statement1 += ' from boxoffice where boxoffice.released < \"%s\" order by released asc;' % (year)

    cursor.execute(statement1)
    results = cursor.fetchall()
    title =[x[0] for x in results]
    released = [x[1] for x in results]
    totalGross = num.array([x[2] for x in results],dtype=float)
    budget = num.array([x[3] for x in results],dtype=float)

    OutMetric = num.log10(totalGross/budget)
    indx_zeros = num.where(OutMetric == num.float('-inf'))[0]
    OutMetric[indx_zeros] = 0e0

    return released,title,OutMetric

def getResponseTest(year='2006-12-31'):
    """   """

    cursor = dbConnect()
    statement1 = 'select title,released,ifnull(totalgross,0),ifnull(budget,0)'
    statement1 += ' from boxoffice where boxoffice.released >= \"%s\" order by released asc;' % (year)

    cursor.execute(statement1)
    results = cursor.fetchall()
    title =[x[0] for x in results]
    released = [x[1] for x in results]
    totalGross = num.array([x[2] for x in results],dtype=float)
    budget = num.array([x[3] for x in results],dtype=float)

    OutMetric = num.log10(totalGross/budget)
    indx_zeros = num.where(OutMetric == num.float('-inf'))[0]
    OutMetric[indx_zeros] = 0e0

    return released,title,OutMetric


def assignInfluenceWeight(partType):
    """ weight the influence """

    weightLevel = 0.0
    if partType == 'Director':
        weightLevel = 1.0
    elif partType == 'Actors':
        weightLevel = 0.75
    elif partType == 'Writer':
        weightLevel = 0.5
    elif partType == 'Genre':
        weightLevel = 0.25
    else:
        pass

    return weightLevel

def InfluenceMultiplier(partHistory,MovieTitles,activeYears):
    """ given the history of participation (partHistory)
        computes the influence level of a given component.
    """

    InfluenceArray = num.zeros(len(activeYears))

    for movieName in MovieTitles:
        weight = 0.0
        for partType in partHistory[movieName]:
            weight += assignInfluenceWeight(partType)
        
        movieYear = getYear(getReleaseDateMovie(movieName).strftime("%Y-%m-%d"))
        indx = num.where(activeYears == int(movieYear))

        InfluenceArray[indx] += weight

    return InfluenceArray


class person:

    def __init__(self, name):

        self.name = name
        self._get_history()

    def _get_history(self):

        # get release dates and Earnings factors from database
        self.ReleaseDates, self.EarningsFactor,\
        self.MovieTitles = getInfluenceHistory(self.name)

        # make an array of only the years of release
        self.ReleaseYears = \
            [int(getYear(RDate.strftime("%Y-%m-%d"))) for RDate in self.ReleaseDates]

        # find the first and last years in which a release was made
        min_date = int(getYear(min(self.ReleaseDates).strftime("%Y-%m-%d")))
        max_date = int(getYear(max(self.ReleaseDates).strftime("%Y-%m-%d")))

        # make an evenly spaced array of years between 
        self.activeYears = num.arange(min_date,max_date+1,1)
        # the first active and last active year as attributes
        self.Year_of_FirstRelease = min_date
        self.Year_of_LastRelease = max_date+1

        # get the dictionary of various participations 
        # of given person
        partHist = getPartHistory(self.name)
        self.InfluenceMultiplier = InfluenceMultiplier(partHist,self.MovieTitles,self.activeYears)
        # print len(self.InfluenceMultiplier), len(self.EarningsFactor), len(self.ReleaseDates), len(self.ReleaseYears)

    def computeInfluenceHistory(self,half_life=3.0):
        """ compute the Influence History """

        self.half_life = num.float(half_life)

        # for i in range(len(self.EarningsFactor)):
        #     print self.ReleaseYears[i], self.EarningsFactor[i]

        activeYearlyEarnings = \
            num.array([num.sum(self.EarningsFactor[num.where(self.ReleaseYears ==\
             yy)[0]]) for yy in self.activeYears])

        # print activeYearlyEarnings
        activeYearlyEarnings *= self.InfluenceMultiplier

        InfluenceFactor = []
        for i in xrange(len(self.activeYears)):
            if i == 0:
                decay = 1.0
                InfluenceFactor.append(activeYearlyEarnings[i])
            else:
                delta_time = self.activeYears[i]-self.activeYears[i-1]
                decay = (0.5)**(delta_time/self.half_life)
                InfluenceFactor.append(InfluenceFactor[-1]*decay + activeYearlyEarnings[i])

        self.InfluenceFactor = num.array(InfluenceFactor)

    def influence_by_year(self,year=2013):
        """ returns the influence for a give year """

        influence = 0.0
        if year < self.Year_of_FirstRelease:
            pass
        elif year > self.Year_of_LastRelease:
            delta_time = year - self.Year_of_LastRelease
            decay = (0.5)**(delta_time/self.half_life)
            influence = self.InfluenceFactor[-1]*decay
        else:
            idx_year = num.where(self.activeYears == year)[0]
            influence = self.InfluenceFactor[idx_year]

        return influence[0]

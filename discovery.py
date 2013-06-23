
import numpy as num
from flopbuster.misc import getYear
# from readdb import dbConnect

def retriveResponse(year='2006-12-31',is_training=True):
    """  Given the year of division, return the list of all movies
         and the SuccessMetric """

    if is_training:
        greater_less_symbol = '<'
    else:
        greater_less_symbol = '>'

    statement1 = 'select title,released,ifnull(totalgross,0),'+\
                 'ifnull(budget,0)'+\
                 ' from boxoffice where boxoffice.released'+\
                 ' %s \"%s\" order by released asc;'
    
    results = mysqlfuncs.db_execute_and_fetch(statement1)
    title = mysqlfuncs.results_to_list(results,index=0)
    released = mysqlfuncs.results_to_list(results,index=1)

    totalGross = num.array(results_to_list(results,index=2),dtype=float)
    budget = num.array(results_to_list(results,index=3),dtype=float)
    SuccessMetric = num.log10(totalGross/budget)

    # replace impossible metrics with zeros
    indx_zeros = num.where(SuccessMetric == num.float('-inf'))[0]
    SuccessMetric[indx_zeros] = 0e0

    return released,title,SuccessMetric

def assignInfluenceWeight(partType):
    """ weight the influence """

    weightLevel = 0.0
    if partType == 'Director':
        weightLevel = 2.0
    elif partType == 'Actors':
        weightLevel = 1.0
    elif partType == 'Writer':
        weightLevel = 0.5
    elif partType == 'Genre':
        weightLevel = 1.5
    else:
        pass

    return weightLevel


class feature:

    def __init__(self, featureName):

        self.name = name
        self._get_history()

    def add_Response(self, is_training=True):

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


#------
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

###---------------------------------------###


from flopbuster.mysqlfuncs import get_successMetric_history
from flopbuster.misc import getYear

class feature:

    def __init__(self, name):

        self.name = name
        self._get_history()

    def _get_history(self):

        # get release dates and Earnings factors from database
        self.ReleaseDates, self.EarningsFactor,\
        self.MovieTitles = get_successMetric_history(self.name)

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

### ------------------------------- ###


# from flopbuster.discovery import getResponseTraining
# from flopbuster.discovery import getResponseTest, getFeatureSet
# from flopbuster.readdb import getTitlesByPart, getTitlesByPartTest
# from flopbuster.readdb import getInfluenceByYearPart
from flopbuster.misc import getYear
import numpy as num

DEFAULT_YearDivide = '2006-01-31'

class ml_dataset:

    def __init__(self, yearDivide=DEFAULT_YearDivide):
        self.yearDivide = yearDivide

    def makeTraining(self):

        RD,Titles,Response = getResponseTraining(year=self.yearDivide)
        
        self.release_dates = [getYear(RDate.strftime("%Y-%m-%d")) for RDate in RD]
        self.titles = Titles
        self.response = Response
        self.SetType = 'training'
        self._remainingPrep()

    def makeTest(self):

        RD,Titles,Response = getResponseTest(year=self.yearDivide)
        self.release_dates = [getYear(RDate.strftime("%Y-%m-%d")) for RDate in RD]
        self.titles = Titles
        self.response = Response
        self.SetType = 'test'
        self._remainingPrep()

    def _remainingPrep(self, **kwargs):

        # extract the years from the release date
        get_year_vectorize = num.vectorize(getYear)
        self.years = get_year_vectorize(self.release_dates)

        # get feature set (inherits the keyword set for getFeatureSet in readdb)
        self.featureNames = getFeatureSet(**kwargs)

        # make an empty array of the feature matrix
        self.nfeatures = len(self.featureNames)
        self.nresponse = len(self.response)

        # Creating look-up dictionaries for quick look-up by indices
        FeatureIndex = range(self.nfeatures)
        ResponseIndex = range(self.nresponse)

        self.ReleaseDateDict = dict(zip(ResponseIndex,self.release_dates))
        self.TitleDict = dict(zip(ResponseIndex,self.titles))
        self.ReverseTitleDict = dict(zip(self.titles,ResponseIndex))

        self.ResponseDict = dict(zip(ResponseIndex,self.response))
        self.YearDict = dict(zip(ResponseIndex,self.years))

        self.FeatureDict = dict(zip(FeatureIndex,self.featureNames))
        self.ReverseFeatureDict = dict(zip(self.featureNames,FeatureIndex))

    def FeatureSet(self,populate='binary'):
        """ Make the FeatureSetMatrix """

        FeatureSetMatrix = num.zeros((self.nresponse,self.nfeatures))

        for iFeature in self.FeatureDict.keys():
            if self.SetType == 'training':
                TitleList = getTitlesByPart(self.FeatureDict[iFeature],self.yearDivide)
            else:
                TitleList = getTitlesByPartTest(self.FeatureDict[iFeature],self.yearDivide)

            for title in TitleList:
                iResponse = self.ReverseTitleDict[title]
                print title, iResponse
                if populate == 'binary':
                    FeatureSetMatrix[iResponse][iFeature] = 1.0
                elif populate == 'influence':
                    influence = getInfluenceByYearPart(self.FeatureDict[iFeature],\
                                self.YearDict[iResponse])
                    FeatureSetMatrix[iResponse][iFeature] = influence
                else:
                    print 'populate option not recognized'

        self.FeatureSetMatrix = FeatureSetMatrix


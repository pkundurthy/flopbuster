
import numpy as num
from flopbuster import mysqlfuncs
from flopbuster import misc

DEFAULT_YearDivide = '2006-12-31'
DEFAULT_halflife = 3.0

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

def retriveResponse(year=DEFAULT_YearDivide,is_training=True):
    """ Given the year dividing training and test sets, return the list of 
        all movies and the SuccessMetric """

    if is_training:
        comp_symbol = '<'
    else:
        comp_symbol = '>'

    statement1 = 'select title,released,ifnull(totalgross,0),'+\
                 'ifnull(budget,0)'+\
                 ' from boxoffice where boxoffice.released'+\
                 ' %s \"%s\" order by released asc;' % (comp_symbol,year)
    
    results = mysqlfuncs.db_execute_and_fetch(statement1)
    title = mysqlfuncs.results_to_list(results,index=0)
    released = mysqlfuncs.results_to_list(results,index=1)
    releaseYears = [long(misc.getYear(x.strftime("%Y-%m-%d"))) for x in released]

    totalGross = num.array(mysqlfuncs.results_to_list(results,index=2),\
                            dtype=float)
    budget = num.array(mysqlfuncs.results_to_list(results,index=3),dtype=float)
    SuccessMetric = num.log10(totalGross/budget)

    # replace impossible metrics with zeros
    indx_zeros = num.where(SuccessMetric == num.float('-inf'))[0]
    SuccessMetric[indx_zeros] = 0e0

    return releaseYears,title,SuccessMetric

def InfluenceMultiplier(partHist,titles):
    """ returns array of influence multiplier factors to scale 
        partipant's influence level by role """

    # Initiate Influence multiplier array
    InfluenceMultiArray = []
    for i in xrange(len(titles)):
        movieName = titles[i]
        influence_num = 0.0
        for partType in partHist[movieName]:
            influence_num += assignInfluenceWeight(partType)

        InfluenceMultiArray.append(influence_num)

    return InfluenceMultiArray

def get_FeatureSet(partTypes=None):
    """ return a given FeatureSet/part(s) 
        keyword option partTypes is either None or a list
        of partTypes 
    """

    if partTypes == None:
        appendStatement = ''
    else:
        appendStatement = 'where( '
        appendStatement += \
        ' or '.join(['partType = '+'\"'+x+'\"' for x in partTypes])
        appendStatement += ')'

    statement1 = 'select distinct(part) from movie_meta '
    statement1 += appendStatement
    statement1 += ' order by part asc;'

    results = mysqlfuncs.db_execute_and_fetch(statement1)
    FeatureSet = mysqlfuncs.results_to_list(results,index=0)
    return FeatureSet

class feature:

    def __init__(self, FeatureName):

        self.name = FeatureName
        self._history()

    def _history(self):

        # get release dates, titles and successMetric from database
        self.ReleaseDates, self.successMetric, self.MovieTitles = \
                         mysqlfuncs.get_successMetric_history(self.name)

        # make an array of only the years of release
        self.ReleaseYears = [int(misc.getYear(RDate.strftime("%Y-%m-%d")))\
                             for RDate in self.ReleaseDates]

        # find the first and last years in which a release was made
        min_date = min(self.ReleaseDates).strftime("%Y-%m-%d")
        max_date = max(self.ReleaseDates).strftime("%Y-%m-%d")
        min_date = int(misc.getYear(min_date))
        max_date = int(misc.getYear(max_date))

        # the first active and last active year as attributes
        self.Year_of_FirstRelease = min_date
        self.Year_of_LastRelease = max_date+1

        # get the dictionary of various participations 
        # of given person
        partHist = \
            mysqlfuncs.get_title_partType_byPart(self.name)

        self.InfluenceMultiplier = \
            InfluenceMultiplier(partHist,self.MovieTitles)

    def computeProfitability(self,half_life=DEFAULT_halflife):
        
        self.half_life = num.float(half_life)
        profitability = []
        yearImpact = {}
        for i in range(len(self.MovieTitles)-1):
            if yearImpact.has_key(self.ReleaseYears[i]):
                yearImpact[self.ReleaseYears[i]] += \
                     self.successMetric[i]
            else:
                yearImpact[self.ReleaseYears[i]] = \
                     self.successMetric[i]

        yProf = num.array(yearImpact.keys())
        Prof = num.array(yearImpact.values())
        indxsort = yProf.argsort()
        self.yearProfit = yProf[indxsort]
        self.profit = Prof[indxsort]




    def computeInfluenceHistory(self,half_life=DEFAULT_halflife,currentYear=2013):

        self.half_life = num.float(half_life)
        Impact = []
        decay_list = []
        yearImpact = []
        # run through all the years for each movie title
        for i in range(len(self.MovieTitles)-1):
            impactNumber = self.InfluenceMultiplier[i]*\
                              self.successMetric[i]
            # if the given release year is equal to the year 
            # of debut then set decay to newbie setting
            if self.ReleaseYears[i] == self.Year_of_FirstRelease:
                delta_time = 3.0
                decay = (0.5)**(delta_time/self.half_life)
                # check for multiple released during debut year
                if len(Impact) != 0:
                    Impact[-1] += impactNumber
                else:
                    Impact.append(impactNumber*decay)
                    decay_list.append(decay)
                    yearImpact.append(self.ReleaseYears[i])
            elif self.ReleaseYears[i] > self.Year_of_LastRelease:
                # this should never happen, since feature object
                # aggregates all the data for a given feature
                raise NameError("release date is after last release")
            else:
                # for all other cases than the debut year release
                delta_time = self.ReleaseYears[i]-self.ReleaseYears[i-1]
                decay = (0.5)**(delta_time/self.half_life)
                # check for multiple releases
                if delta_time == 0.0:
                    Impact[-1] += impactNumber
                else:
                    Impact.append(Impact[-1]*decay + impactNumber)
                    decay_list.append(decay)
                    yearImpact.append(self.ReleaseYears[i])
        

        self.decay_list = decay_list
        self.yearImpact = yearImpact
        self.Impact = Impact



import numpy as num
from flopbuster import mysqlfuncs
from flopbuster import misc

DEFAULT_YearDivide = '2006-12-31'

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

    # def computeInfluenceHistory(self,half_life=3.0):

    #     self.half_life = num.float(half_life)

    #     for i in range(len(self.MovieTitles)):
    #         delta_time = 
    #         if self.ReleaseDates[i] == self.Year_of_FirstRelease:
    #             delta_time = 0.0
    #         elif self.ReleaseDates[i] > self.Year_of_LastRelease:
    #             delta_time = 
    #         else:
    #             delta_time = self.ReleaseDates[i+1]-self.ReleaseDates[i]

    #         decay = (0.5)**(delta_time/self.half_life)




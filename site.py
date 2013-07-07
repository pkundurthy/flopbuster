import numpy as num
from flopbuster import misc
from flopbuster import mysqlfuncs
from flopbuster import ML_prep
import os, re
module_path = os.path.dirname(__file__)+'/'

chart_script_lines = open(module_path+'gen_chart_data','r').readlines()
barchart_script_lines = open(module_path+'gen_bar_data','r').readlines()


def tens_letter(nzeros):
    """  compress large boxoffice numbers  """

    outLetter = ' '
    if nzeros == 6:
        outLetter = ' Million'
    if nzeros == 9:
        outLetter = ' Billion'

    return outLetter

def million_billion_format(number):
    """ converting large box-office numbers to readable format """

    strLen = len(format(number,'.0f'))

    if strLen > 9:
        nzeros = 9
        OutStr = format(number/1E9,'.1f')
    elif strLen > 6:
        nzeros = 6
        OutStr = format(number/1E6,'.0f')
    else:
        nzeros = 0
        OutStr = format(number/1E3,'.0f')+',000'

    OutStr += tens_letter(nzeros)

    return OutStr

def MovieBudget(movieName,movieYear):
    """ retrive the budget for a given movie, and the year of make """

    statement1 = 'select released,title,budget from boxoffice'
    statement1 += ' where (title = \"%s\");' % movieName

    results = mysqlfuncs.db_execute_and_fetch(statement1)
    yearUnformatted = mysqlfuncs.results_to_list(results,index=0)
    yearReleased = num.array([long(misc.getYear(x.strftime("%Y-%m-%d"))) \
                    for x in yearUnformatted])

    titles = mysqlfuncs.results_to_list(results,index=1)
    budgets = num.array(mysqlfuncs.results_to_list(results,index=2))

    # remove title ambiguiities by matching the release year
    if len(yearReleased) > 1:
        idx = num.where(yearReleased = movieYear)[0]
    else:
        idx = 0

    return budgets[idx]


def printCashString(ActualGross,PredictedGross,Budget):
    """ return cash numbers in string format """

    Act_String, Pred_String, Budget_String = 'Unknown','Unkown','Unkown'
    if Budget == 0:
        pass
    else:
        Act_String = '$'+million_billion_format(ActualGross)
        Pred_String = '$'+million_billion_format(PredictedGross)
        Budget_String = '$'+million_billion_format(Budget)

    return Act_String,Pred_String,Budget_String

def MovieComparison(movieName):
    """ Retrive actual movie gross, the predicted gross and budget
        for a given movie. """

    # setup query statement
    statement1 = 'select year,predicted,actual '
    statement1 += 'from Property001 where (title = \"%s\");' % movieName

    results = mysqlfuncs.db_execute_and_fetch(statement1)
    
    yearUnformatted = mysqlfuncs.results_to_list(results,index=0)
    year = [long(misc.getYear(x.strftime('%Y-%m-%d'))) for x in yearUnformatted]

    predictedFactor = mysqlfuncs.results_to_list(results,index=1)
    actualFactor = mysqlfuncs.results_to_list(results,index=2)
    Budget, ActualGross, PredictedGross = 0,0,0
    try:
        Budget = MovieBudget(movieName,year[0])
        ActualGross = 10**(actualFactor[0]) * Budget
        PredictedGross = 10**(predictedFactor[0]) * Budget
    except:
        pass

    # convert to currency string format for output to page
    # ActualGross =  '{:20,.0f}'.format(10**(actualFactor[0]) * budget)
    # PredictedGross = '{:20,.0f}'.format(10**(predictedFactor[0]) * budget)
    # BudgetString = '{:20,.0f}'.format(budget)
    return ActualGross, PredictedGross, Budget

def compileMovieData(movieName):
    """ Compile printable JSON-like dictionary to print movie meta-data
        to webpage. """

    # setup statements to get info about Directors, Actors, Writers and Genre
    # for a given movie.
    statementRoot = 'select distinct(part) from movie_meta where '
    statement1 = statementRoot+'(partType = \"Director\" and title = \"%s\");'\
                % (movieName)
    statement2 = statementRoot+'(partType = \"Actors\" and title = \"%s\");'\
                % (movieName)
    statement3 = statementRoot+'(partType = \"Writer\" and title = \"%s\");'\
                % (movieName)
    statement4 = statementRoot+'(partType = \"Genre\" and title = \"%s\");'\
                % (movieName)
    
    # get results for query for directors, actors, writers and genre
    results1 = mysqlfuncs.db_execute_and_fetch(statement1)
    results2 = mysqlfuncs.db_execute_and_fetch(statement2)
    results3 = mysqlfuncs.db_execute_and_fetch(statement3)
    results4 = mysqlfuncs.db_execute_and_fetch(statement4)

    Directors = mysqlfuncs.results_to_list(results1,index=0)
    Actors = mysqlfuncs.results_to_list(results2,index=0)
    Writers = mysqlfuncs.results_to_list(results3,index=0)
    Genre = mysqlfuncs.results_to_list(results4,index=0)

    outDict =  {'Director(s)':Directors,'Actor(s)':Actors,\
            'Writer(s)':Writers,'Genre':Genre}
    return outDict

def generate_selected_features(outDict):
    """ generate the profitability plot on the webpage """

    featureList = []
    for key in ['Director(s)','Actor(s)']:
        lenF = len(outDict[key])
        for i in range(lenF):
            if key == 'Actor(s)' and i <= 3:
                featureList.append(outDict[key][i])
            elif key == 'Actor(s)' and i > 3:
                pass
            else:
                featureList.append(outDict[key][i])

    return featureList

def make_chart_data(featureName):
    """ make series List  """

    featureObject = ML_prep.feature(featureName)
    featureObject.computeProfitability()
    featureObject.computeImpactHistory()

    dataList = []
    for i in range(len(featureObject.Impact)):
        dataList.append([featureObject.yearImpact[i],\
                        featureObject.Impact[i]])
    seriesString = '{name:\"'+featureObject.name+'\",'

    movieListString = ','.join(['\"'+x+'\"' for x in featureObject.MovieTitles])
    dataListString = str(dataList)
    seriesString += ' id:['+movieListString+'],'
    seriesString += ' data:'+dataListString+'}'

    return seriesString

def make_chart_point(featureName):

    featureObject = ML_prep.feature(featureName)
    featureObject.computeProfitability()
    featureObject.computeImpactHistory()
    movieListString = ','.join(['\"'+x+'\"' for x in featureObject.MovieTitles])
    return movieListString

def generate_chart(outDict,movieName):
    """ make chart script file """

    titleLine = 'title:{text: \"%s\"},' % (movieName)
    featureList = generate_selected_features(outDict)
    outFile = open(module_path+'/site/static/js/profitability.js','w')

    seriesList = [make_chart_data(x) for x in featureList]
    movieList = [make_chart_point(x) for x in featureList]

    for line in chart_script_lines:
        if line.startswith('#title'):
            print >> outFile, titleLine
        elif line.startswith('#data'):
            seriesListString = str(seriesList)
            seriesListString = re.sub("'","",seriesListString)
            print >> outFile, 'series: '+seriesListString
        elif line.startswith('#point'):
            movieListString = str(movieList)
            print >> outFile, 'point: '+movieListString
        else:
            print >> outFile, line.strip('\n')

    outFile.close()

def generate_bar_chart(Actual,Predicted,Budget):
    """ the function that generates the comparison bar chart """

    outFile = open(module_path+'site/static/js/barchart.js','w')

    Act_String, Pred_String, Budget_String = \
        printCashString(Actual,Predicted,Budget)

    outLine = \
        'series: [ { name:\'Actual %s \', data: [%s] }, ' % (Act_String,Actual)
    outLine += \
        '{ name:\'Predicted %s \', data: [%s] },' % (Pred_String,Predicted)
    outLine += \
        '{ name:\'Budget %s \', data: [%s] } ]' % (Budget_String,Budget)

    for line in barchart_script_lines:
        if line.startswith('#data'):
            print >> outFile, outLine
        else:
            print >> outFile, line.strip('\n')

    outFile.close()

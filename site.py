import numpy as num
from flopbuster import misc
from flopbuster import mysqlfuncs


def tens_letter(nzeros):
    """             """

    outLetter = ' '
    if nzeros == 6:
        outLetter = ' Million'
    if nzeros == 9:
        outLetter = ' Billion'

    return outLetter

def million_billion_format(number):
    """ convertion large box-office numbers to readable format """

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
    budget = MovieBudget(movieName,year[0])

    ActualGross = million_billion_format(10**(actualFactor[0]) * budget)
    PredictedGross = million_billion_format(10**(predictedFactor[0]) * budget)
    BudgetString = million_billion_format(budget)

    # convert to currency string format for output to page
    # ActualGross =  '{:20,.0f}'.format(10**(actualFactor[0]) * budget)
    # PredictedGross = '{:20,.0f}'.format(10**(predictedFactor[0]) * budget)
    # BudgetString = '{:20,.0f}'.format(budget)
    return ActualGross, PredictedGross, BudgetString

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












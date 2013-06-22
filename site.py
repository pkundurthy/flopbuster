import MySQLdb
from flopbuster.misc import getYear
from flopbuster.readdb import dbConnect
import numpy as num

def getBudget(movieName,movieYear):
    """                          """

    cursor = dbConnect()

    statement1 = 'select released,title,budget from boxoffice'
    statement1 += ' where (title = \"%s\");' % movieName

    cursor.execute(statement1)
    results = cursor.fetchall()

    yearReleased = num.array([long(getYear(x[0].strftime("%Y-%m-%d"))) for x in results])
    titles =  [x[1] for x in results]
    budgets = num.array([x[2] for x in results])
    
    if len(yearReleased) > 1:
        idx = num.where(yearReleased = movieYear)[0]
    else:
        idx = 0

    return budgets[0]

def MovieComparison(movieName):
    """                     """

    cursor = dbConnect()
    statement1 = 'select year,predicted,actual '
    statement1 += 'from Property001 where (title = \"%s\");' % movieName

    cursor.execute(statement1)
    results = cursor.fetchall()
    
    year = [long(getYear(x[0].strftime('%Y-%m-%d'))) for x in results]
    predictedFactor = [x[1] for x in results]
    actualFactor = [x[2] for x in results]

    budget = getBudget(movieName,year[0])
    
    ActualGross =  '{:20,.0f}'.format(10**(actualFactor[0]) * budget)
    PredictedGross = '{:20,.0f}'.format(10**(predictedFactor[0]) * budget)
    BudgetString = '{:20,.0f}'.format(budget)
    return ActualGross, PredictedGross, BudgetString


def compileMovieData(movieName):
    """                             """

    cursor = dbConnect()
    statementRoot = 'select distinct(part) from movie_meta where '
    statement1 = statementRoot+'(partType = \"Director\" and title = \"%s\");' % (movieName)
    statement2 = statementRoot+'(partType = \"Actors\" and title = \"%s\");' % (movieName)
    statement3 = statementRoot+'(partType = \"Writer\" and title = \"%s\");' % (movieName)
    statement4 = statementRoot+'(partType = \"Genre\" and title = \"%s\");' % (movieName)
    
    cursor.execute(statement1)
    results1 = cursor.fetchall()
    Directors = [x[0] for x in results1]

    cursor.execute(statement2)
    results2 = cursor.fetchall()
    Actors = [x[0] for x in results2]

    cursor.execute(statement3)
    results3 = cursor.fetchall()
    Writers = [x[0] for x in results3]

    cursor.execute(statement4)
    results4 = cursor.fetchall()
    Genre = [x[0] for x in results4]

    out =  {'Director(s)':Directors,'Actor(s)':Actors,\
            'Writer(s)':Writers,'Genre':Genre}
    return out












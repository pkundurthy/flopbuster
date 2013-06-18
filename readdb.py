

import MySQLdb
import numpy as num
import cPickle
import unicodedata

def_dBhost = 'localhost'
def_dBuser = 'root'
def_dBpass = ''
def_dBname = 'flopbuster'
def_path_to_socket = '/var/mysql/mysql.sock'


def dbConnect(dBhost=def_dBhost,dBuser=def_dBuser,\
              dBpass=def_dBpass,dBname=def_dBname,\
              path_to_socket=def_path_to_socket):
    """ standard MySQLdb connector to 'flopbuster' database """
    
    db = MySQLdb.connect(host=dBhost, user=dBuser,\
                         passwd=dBpass,db=dBname,unix_socket=path_to_socket)
    cursor = db.cursor()
    return cursor

def getTitles_BoxOffice():
    """
        get list of all movie titles from boxoffice table
    """

    cursor = dbConnect()
    foo  = 'select title from boxoffice;'
    cursor.execute(foo)
    results = cursor.fetchall()

    return [x[0] for x in results]


def getGrosses_BoxOffice(notNulls=['budget','usgross','worldgross']):
    """
        This function will return the budget, US gross, Worldwide Gross and
        Movie title from the Box Office database. The notNulls keyword sets 
        whether null information from a given column is used to filter out
        results. e.g. if notNulls=['budget','worldgross'], the resulting table 
        will only include those movies where 'budget' and 'worldgross' are not
        NULLs.
    """
    
    cursor = dbConnect()
    foo = 'select budget,usgross,worldgross,title from boxoffice'
    foo += ' where( '
    foo += ' and '.join([x+' is not NULL' for x in notNulls])
    foo += ');'

    cursor.execute(foo)
    results = cursor.fetchall()

    budget = num.array([x[0] for x in results])
    usgross = num.array([x[1] for x in results])
    worldgross = num.array([x[2] for x in results])
    title = [x[3] for x in results]

    return budget,usgross,worldgross,title

# app = Flask(__name__, template_folder=tmpl_dir)
# oFile = open('OutDict.pickle','rb')
# oFile = open('OutDict.pickle','rb')
# ResultsDict = cPickle.load(oFile)

def getSucessString(sNumber):

    sNumber = long(sNumber)
    if sNumber == -1:
        oStr = 'Fail!'
    elif sNumber == 0:
        oStr = '(meh) did ok...'
    elif sNumber == 1:
        oStr = 'Good!'
    elif sNumber == 2:
        oStr = 'Awesome! $$'
    else:
        oStr = 'Unknown'

    return oStr

def grabMovieComparison(movieName):

    # print movieName, ResultsDict
    mName = unicodedata.normalize('NFKD', movieName).encode('ascii','ignore')

    # ActualSucess = getSucessString(ResultsDict[mName]['Actual'])
    # PredictedSucess = getSucessString(ResultsDict[mName]['Predicted'])
    ActualSucess = getSucessString(ResultsDict[mName]['Actual'])
    PredictedSucess = getSucessString(ResultsDict[mName]['Predicted'])
    return [mName,PredictedSucess,ActualSucess]


# # def getInstance_BoxOfficeMovie(MovieName, countEntry=False):
# #     """
# #         find all data on a given movie title from BoxOffice table.
# #         countEntry=True will return the number of rows for a given
# #         match to MovieName string.
# #     """

# #     foo  = 'select title from boxoffice;' % (MovieName)
# #     cursor.execute(foo)

# #     print foo

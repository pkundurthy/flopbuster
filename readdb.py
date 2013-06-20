

import MySQLdb
import numpy as num
num.seterr(divide='ignore')
import cPickle
import datetime
import unicodedata

def_dBhost = 'localhost'
def_dBuser = 'root'
def_dBpass = ''
def_dBname = 'flopbuster'
def_path_to_socket = '/var/mysql/mysql.sock'

def dbConnect(dBhost=def_dBhost,dBuser=def_dBuser,\
              dBpass=def_dBpass,dBname=def_dBname,\
              path_to_socket=def_path_to_socket):
    """ the basic MySQLdb connector to the 'flopbuster' database """
    
    db = MySQLdb.connect(host=dBhost, user=dBuser,\
                         passwd=dBpass,db=dBname,unix_socket=path_to_socket)
    cursor = db.cursor()
    return cursor

def getTitles_BoxOffice():
    """ get list of all movie titles from boxoffice table """

    cursor = dbConnect()
    foo  = 'select title from boxoffice;'
    cursor.execute(foo)
    results = cursor.fetchall()

    return [x[0] for x in results]

def getGrosses_BoxOffice(notNulls=['budget','usgross','worldgross']):
    """ A function to return the budget, US gross, Worldwide Gross and
        Movie title from the Box Office database. 

        notNulls (keyword) sets is used to filter out nulls form the columns
        presented in the list. For e.g. if notNulls=['budget','worldgross'], 
        the resulting table will only include those movies where 'budget' and
        'worldgross' are not NULLs. """
    
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

def getReleaseDateMovie(movieName):
    """ get the date of release of a movie """

    cursor = dbConnect()
    statement1 = 'select released from boxoffice where title = "%s" ' % (movieName)
    cursor.execute(statement1)
    results = cursor.fetchall()
    release_date = [x[0] for x in results]
    return release_date[0]

def getInfluenceHistory(person):
    """ get the Influence history of given person """

    cursor = dbConnect()
    statement1 = 'select title,released,ifnull(totalgross,0),ifnull(budget,0)'
    statement1 += ' from boxoffice where boxoffice.title = any '
    statement1 += '(select `title` from movie_meta '
    statement1 += 'where(part = "%s")) order by released asc;' % (person)

    cursor.execute(statement1)
    results = cursor.fetchall()
    title =[x[0] for x in results]
    release = [x[1] for x in results]
    totalGross = num.array([x[2] for x in results],dtype=float)
    budget = num.array([x[3] for x in results],dtype=float)

    OutMetric = num.log10(totalGross/budget)
    indx_zeros = num.where(OutMetric == num.float('-inf'))[0]
    OutMetric[indx_zeros] = 0e0

    return release,OutMetric,title

def getPartHistory(personName):
    """ get the list of roles played by a given person """

    cursor = dbConnect()
    statement1 = "select title, partType from movie_meta where movie_meta.part = \"%s\";" % (personName)

    cursor.execute(statement1)
    results = cursor.fetchall()
    titles = [x[0] for x in results]
    partType = [x[1] for x in results]
    partHist = {}
    for i in range(len(titles)):
        if partHist.has_key(titles[i]):
            partHist[titles[i]].append(partType[i])
        else:
            partHist[titles[i]] = [partType[i]]

    return partHist

def getAllGrossFactor():

    cursor = dbConnect()
    statement1 = 'select released,ifnull(totalgross,0),budget from boxoffice;'

    cursor.execute(statement1)
    results = cursor.fetchall()
    release = [x[0] for x in results]
    totalGross = num.array([x[1] for x in results])
    budget = num.array([x[2] for x in results])

    return release,totalGross/budget

def getInOutMoney():

    cursor = dbConnect()
    statement1 = 'select ifnull(totalgross,0),budget from boxoffice;'
    cursor.execute(statement1)
    results = cursor.fetchall()
    totalGross = num.array([x[0] for x in results])
    budget = num.array([x[1] for x in results])

    return budget,totalGross

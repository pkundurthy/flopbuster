
import MySQLdb
import numpy as num
num.seterr(divide='ignore')
import cPickle
import datetime
import unicodedata
import os
import socket
module_path = os.path.dirname(__file__)+'/'

DB_CONNECTION_INFO = cPickle.load(open(module_path+'DBCONNECT.pickle','rb'))
unidef_dB_host = DB_CONNECTION_INFO['dbHost']
unidef_dB_user = DB_CONNECTION_INFO['dbUser']
unidef_dB_pass = DB_CONNECTION_INFO['dbPass']
unidef_dB_name = DB_CONNECTION_INFO['dbName']

if socket.gethostbyname(socket.gethostname()).startswith('192'):
    unidef_path_to_socket = DB_CONNECTION_INFO['path_to_socket']
else:
    unidef_path_to_socket = '/var/run/mysqld/mysqld.sock'

## ---- Start section on functions to perform basic db operation --- ##
def db_connect(dBhost=unidef_dB_host,dBuser=unidef_dB_user,\
              dBpass=unidef_dB_pass,dBname=unidef_dB_name,\
              path_to_socket=unidef_path_to_socket):
    """ the basic MySQLdb connector to the 'flopbuster' database  """
    
    db = MySQLdb.connect(host=dBhost, user=dBuser,\
                     passwd=dBpass,db=dBname,unix_socket=path_to_socket)
    cursor = db.cursor()
    return cursor

def db_execute_and_fetch(statement):
    """ execute statement on cursor and fetchall results"""

    cursor = db_connect()
    cursor.execute(statement)
    results = cursor.fetchall()
    return results

def results_to_list(results,index=0):
    """ perform list comprehension and return results """

    return [x[index] for x in results]

## --- Start section on functions related to the boxoffice table --- ##
def get_titles_boxoffice():
    """ get list of all movie titles from boxoffice table """
    
    statement1  = 'select title from boxoffice;'
    titles = results_to_list(db_execute_and_fetch(statement1),index=0)

    return titles

def get_grosses_boxoffice(notNulls=['budget','usgross','worldgross']):
    """ A function to return the budget, US gross, Worldwide Gross and
        Movie title from the Box Office database. 

        notNulls (keyword) sets is used to filter out nulls form the columns
        presented in the list. For e.g. if notNulls=['budget','worldgross'], 
        the resulting table will only include those movies where 'budget' and
        'worldgross' are not NULLs. 
    """
    
    # setup the query statement
    statement1 = 'select budget,usgross,worldgross,title from boxoffice'
    statement1 += ' where( '
    # the 'money' fields that should not be null are joined with 'and'
    # in the where condition
    statement1 += ' and '.join([x+' is not NULL' for x in notNulls])
    statement1 += ');'

    results = db_execute_and_fetch(statement1)

    # get the budget, usgross, world gross and titles
    budget = num.array(results_to_list(results,index=0))
    usgross = num.array(results_to_list(results,index=1))
    worldgross = num.array(results_to_list(results,index=2))
    title = results_to_list(results,index=3)

    return budget,usgross,worldgross,title

def get_released_dates(movieName):
    """ get the date of release of a movie """

    # setup query statement
    statement1 = \
    'select released from boxoffice where title = "%s" ' % (movieName)

    results = db_execute_and_fetch(statement1)

    # WARNING NOTE: will return multiple values if multiple
    # titles with the same name exist
    release_date = results_to_list(results,index=0)
    return release_date[0]

## ----- Start section on functions that work on the `influence` table ----- ##
def get_influence_byYear(part,year):
    """ return the influence number for a given year for a given part. """

    year  = year+'-01-01'
    statement1 = 'select influence from influence where '
    statement1 += '(part = \"%s\" and year = \"%s\");' % (part,year)

    results = db_execute_and_fetch(statement1)
    influence = results_to_list(results,index=0)
    return influence[0]

## ----- Start section on function with complex MySQL queries ----- ##
def get_successMetric_history(person):
    """ get the successMetric and release dates and titles for 
        a given person (also called `part` in moive_meta) """

    # setup the query
    statement1 = 'select title,released,ifnull(totalgross,0),ifnull(budget,0)'
    statement1 += ' from boxoffice where boxoffice.title = any '
    statement1 += '(select `title` from movie_meta '
    statement1 += 'where(part = "%s")) order by released asc;' % (person)

    # get the title, release data, total gross and budget
    results = db_execute_and_fetch(statement1)

    title = results_to_list(results,index=0)
    release = results_to_list(results,index=1)
    totalGross = num.array(results_to_list(results,index=2),dtype=float)
    budget = num.array(results_to_list(results,index=3),dtype=float)

    # compute the sucess metric = log10(totalGross/budget)
    successMetric = totalGross/budget

    # change -inf values to zeros
    indx_zeros = num.where(successMetric == num.float('-inf'))[0]
    successMetric[indx_zeros] = 0e0

    return release,successMetric,title

def get_titles_byPart(part,yearDivide,is_before=True):
    """ for a given part (aka Feature) return the movie titles
        before or after a given year. """

    if is_before:
        greater_less = '<'
    else:
        greater_less = '>'

    statement1 = \
    'select title from boxoffice where released \"%s\" \"%s\"' % \
    (greater_less, yearDivide)
    statement1 += ' and boxoffice.title = any '
    statement1 += '(select title from movie_meta where part = '
    statement1 += ' \"%s\");' % (part)

    results = db_execute_and_fetch(statement1)
    titles = results_to_list(results,index=0)

    return titles

def get_title_partType_byPart(partName):
    """ get the list of roles played by a given person. 
    partHist is a dictionary which returns lists of roles by a given 
    part/Feature for every movie they've taken part in 
    e.g. partName = John Smith
    movies = ['Action Blast I','Depressing Stuff','Action Blast II']
    partHist = {'Action Blast I':['Actor'],\
                'Depressing Stuff':['Writer','Director'],\
                'Action Blast II': ['Actor']} """

    statement1 = \
    "select title, partType from movie_meta where movie_meta.part = \"%s\";" \
    % (partName)

    results = db_execute_and_fetch(statement1)
    titles = results_to_list(results,index=0)
    partType = results_to_list(results,index=1)

    partHist = {}
    for i in range(len(titles)):
        if partHist.has_key(titles[i]):
            partHist[titles[i]].append(partType[i])
        else:
            partHist[titles[i]] = [partType[i]]

    return partHist




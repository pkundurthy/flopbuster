
import MySQLdb
from flopbuster import readdb
from datetime import datetime
import numpy as num

def getInfluenceHistory(person):
    """ get the Influence history of given person """

    cursor = readdb.dbConnect()
    statement1 = 'select title,released,ifnull(totalgross,0),budget'
    statement1 += ' from boxoffice where boxoffice.title = any '
    statement1 += '(select `title` from movie_meta '
    statement1 += 'where(part = "%s")) order by released asc;' % (person)

    cursor.execute(statement1)
    results = cursor.fetchall()
    title =[x[0] for x in results]
    release = [x[1] for x in results]
    totalGross = num.array([x[2] for x in results])
    budget = num.array([x[3] for x in results])

    return release,totalGross/budget


def getAllGrossFactor():

    cursor = readdb.dbConnect()
    statement1 = 'select released,ifnull(totalgross,0),budget from boxoffice;'

    cursor.execute(statement1)
    results = cursor.fetchall()
    release = [x[0] for x in results]
    totalGross = num.array([x[1] for x in results])
    budget = num.array([x[2] for x in results])

    return release,totalGross/budget

def getInOutMoney():

    cursor = readdb.dbConnect()
    statement1 = 'select ifnull(totalgross,0),budget from boxoffice;'
    cursor.execute(statement1)
    results = cursor.fetchall()
    totalGross = num.array([x[0] for x in results])
    budget = num.array([x[1] for x in results])

    return budget,totalGross



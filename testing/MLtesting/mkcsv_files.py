

import MySQLdb
import flopbuster
import sys
import numpy as num
import math
import cPickle
from matplotlib import pylab as plt


def getBudget(movieName,relDate):

    cursor = flopbuster.readdb.dbConnect()
    # print movieName
    statement1 = 'select usgross/budget from boxoffice where (title = "%s" and released = "%s");' % (movieName,relDate)
    # print statement1
    cursor.execute(statement1)
    result1 = cursor.fetchall()
    bm = [x[0] for x in result1]

    return bm[0]

def FreqFeature(feature,movieName):

    cursor = flopbuster.readdb.dbConnect()
    statement1 = 'select distinct(partType) from movie_meta where (title = "%s" and part = "%s");' % (movieName,feature)
    cursor.execute(statement1)
    result1 = cursor.fetchall()
    return len(result1)

def getFeature(movieName):

    cursor = flopbuster.readdb.dbConnect()
    statement1 = 'select part from movie_meta where (title = "%s");' % (movieName)
    cursor.execute(statement1)
    result1 = cursor.fetchall()
    return list(set([x[0] for x in result1]))

def genFDict():

    cursor = flopbuster.readdb.dbConnect()
    statement1 = "select distinct part from \
     movie_meta where (partType = 'Director' \
     or partType = 'Genre') order by part asc;"

    cursor.execute(statement1)
    result1 = cursor.fetchall()
    features = [x[0] for x in result1]

    FDict = {}
    count = 1
    for fe in features:
        FDict[fe] = count
        count += 1

    return FDict

def genMDict():
    # cursor = flopbuster.readdb.dbConnect()
    # statement1 = "select released,title,(usgross-budget)/budget from boxoffice where \
    # (budget is not null and usgross is not null and released < '2006-12-31') order \
    # by released asc into outfile '/Users/praveen/flopbuster/MLtesting/training_prep.csv' \
    # FIELDS TERMINATED BY '|' lines terminated by '\n';"

    cursor = flopbuster.readdb.dbConnect()

    statement1 = "select title,released from boxoffice where (title in (select distinct title \
    from movie_meta where (partType = 'Director' or partType = 'Genre')) and budget \
    is not null and usgross is not null and released < '2006-12-31') order by \
    released asc;"

    cursor.execute(statement1)
    result1 = cursor.fetchall()
    movies = [x[0] for x in result1]
    reldate = [x[1] for x in result1]

    MDict = {}
    Reldate = {}

    count = 1
    for i in range(len(movies)):
        mov = movies[i]
        reld = reldate[i]
        MDict[count] = mov
        Reldate[count] = reld
        count += 1

    return MDict,Reldate

def genMDictTest():
    # (3) generate Movie dict (training) {int:Movie} using "select released,title \
    # ,(usgross-budget)/budget from boxoffice where (title in (select distinct title \
    # from movie_meta where (partType = 'Director' or partType = 'Genre')) and budget \
    # is not null and usgross is not null and released < '2006-12-31') order by \
    # released asc;"
    # statement2 = "select released,title,(usgross-budget)/budget from boxoffice where (budget is \
    # not null and usgross is not null and released >= '2006-12-31') order by released \
    # asc into outfile '/Users/praveen/flopbuster/MLtesting/testing_prep.csv' FIELDS TERMINATED BY \
    # '|' lines terminated by '\n';"



    cursor = flopbuster.readdb.dbConnect()

    statement1 = "select title,released from boxoffice where (title in (select distinct title \
    from movie_meta where (partType = 'Director' or partType = 'Genre')) and budget \
    is not null and usgross is not null and released >= '2006-12-31') order by \
    released asc;"

    cursor.execute(statement1)
    result1 = cursor.fetchall()
    movies = [x[0] for x in result1]
    reldate = [x[1] for x in result1]

    MDictTest = {}
    ReldateTest = {}
    count = 1
    for i in range(len(movies)):
        mov = movies[i]
        reld = reldate[i]
        MDictTest[count] = mov
        ReldateTest[count] = reld
        count += 1

    return MDictTest,ReldateTest

def MetricList(movieList,inDict,dateDict):

    MList = []
    for key in inDict:
        bud = getBudget(inDict[key],dateDict[key])
        MList.append(bud)

    return MList


def sortMetrics(inMetrics):

    inMetrics = [round(math.log(x)) for x in inMetrics]
    newMetric = []
    new = 0
    for i in range(len(inMetrics)):
        if inMetrics[i] < 0:
            new = -1
        elif inMetrics[i] <= 0.5:
            new = 0
        elif inMetrics[i] <= 1:
            new = 1
        elif inMetrics[i] <= 2:
            new = 2
        else:
            pass
        newMetric.append(new)

    return num.array(newMetric)

FDict = genFDict()
MDict,RD = genMDict()
MDictTest,RDTest = genMDictTest()
print len(FDict.keys()), len(MDict.keys()), len(MDictTest.keys())

MetListTraining = num.array(MetricList(MDict.values(),MDict,RD))
MetListTest = num.array(MetricList(MDictTest.values(),MDictTest,RDTest))


MetListTraining = sortMetrics(MetListTraining)
MetListTest = sortMetrics(MetListTest)

mTestCsv = open('mtest.data','w')
for el in MDictTest.keys():
    print >> mTestCsv, el,',',MDictTest[el]
mTestCsv.close()



NMovies = len(MDict.keys())
NFeatures = len(FDict.keys())
NMoviesTest = len(MDictTest.keys())

TrainingArray = num.zeros( (NMovies,NFeatures) )
TestArray = num.zeros( (NMoviesTest,NFeatures) )

for i in MDict.keys():
    movieName = MDict[i]
    print 'Train ', movieName
    totalFeatures = 0
    for feature in getFeature(movieName):
        numB = FreqFeature(feature,movieName)
        totalFeatures += numB

    for feature in getFeature(movieName):
        numB = FreqFeature(feature,movieName)
        try:
            j = FDict[feature]
            TrainingArray[i-1,j-1] = float(numB)/float(totalFeatures)
        except:
            pass

for i in MDictTest.keys():
    movieName = MDictTest[i]
    print 'Test ', movieName
    totalFeatures = 0
    for feature in getFeature(movieName):
        numB = FreqFeature(feature,movieName)
        totalFeatures += numB

    for feature in getFeature(movieName):
        numB = FreqFeature(feature,movieName)
        try:
            j = FDict[feature]
            TestArray[i-1,j-1] = float(numB)/float(totalFeatures)
        except:
            pass

train_file = open('TrainFile.pickle',"wb")
cPickle.dump(TrainingArray, train_file, protocol=2)
train_file.close()

metric_train_file = open('MetricFile_Train.pickle',"wb")
cPickle.dump(MetListTraining, metric_train_file, protocol=2)
metric_train_file.close()

test_file = open('TestFile.pickle',"wb")
cPickle.dump(TestArray, test_file, protocol=2)
test_file.close()

metric_test_file = open('MetricFile_Test.pickle',"wb")
cPickle.dump(MetListTest, metric_test_file, protocol=2)
metric_test_file.close()





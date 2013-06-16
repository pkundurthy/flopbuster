

import cPickle
readFile= open('mtest.data','r').readlines()

OutDict = {}
for line in readFile:

    str_list = map(str, line.split(','))
    movieName = str_list[4].strip('\n')
    movieActual = str_list[1].strip()
    moviePredict = str_list[2].strip()
    OutDict[movieName] = {'Actual':movieActual,'Predicted':moviePredict}

print OutDict.keys()
outFile = open('OutDict.pickle','wb')
cPickle.dump(OutDict,outFile,protocol=2)
outFile.close()

import os

os.system('cp -v OutDict.pickle ~/python/flopbuster/site/templates/')



from flopbuster.discovery import getResponseTraining
from flopbuster.discovery import getResponseTest, getFeatureSet
from flopbuster.readdb import getTitlesByPart, getTitlesByPartTest
from flopbuster.readdb import getInfluenceByYearPart
from flopbuster.misc import getYear
import numpy as num

DEFAULT_YearDivide = '2006-01-31'

class ml_dataset:

    def __init__(self, yearDivide=DEFAULT_YearDivide):
        self.yearDivide = yearDivide

    def makeTraining(self):

        RD,Titles,Response = getResponseTraining(year=self.yearDivide)
        
        self.release_dates = [getYear(RDate.strftime("%Y-%m-%d")) for RDate in RD]
        self.titles = Titles
        self.response = Response
        self.SetType = 'training'
        self._remainingPrep()

    def makeTest(self):

        RD,Titles,Response = getResponseTest(year=self.yearDivide)
        self.release_dates = [getYear(RDate.strftime("%Y-%m-%d")) for RDate in RD]
        self.titles = Titles
        self.response = Response
        self.SetType = 'test'
        self._remainingPrep()

    def _remainingPrep(self, **kwargs):

        # extract the years from the release date
        get_year_vectorize = num.vectorize(getYear)
        self.years = get_year_vectorize(self.release_dates)

        # get feature set (inherits the keyword set for getFeatureSet in readdb)
        self.featureNames = getFeatureSet(**kwargs)

        # make an empty array of the feature matrix
        self.nfeatures = len(self.featureNames)
        self.nresponse = len(self.response)

        # Creating look-up dictionaries for quick look-up by indices
        FeatureIndex = range(self.nfeatures)
        ResponseIndex = range(self.nresponse)

        self.ReleaseDateDict = dict(zip(ResponseIndex,self.release_dates))
        self.TitleDict = dict(zip(ResponseIndex,self.titles))
        self.ReverseTitleDict = dict(zip(self.titles,ResponseIndex))

        self.ResponseDict = dict(zip(ResponseIndex,self.response))
        self.YearDict = dict(zip(ResponseIndex,self.years))

        self.FeatureDict = dict(zip(FeatureIndex,self.featureNames))
        self.ReverseFeatureDict = dict(zip(self.featureNames,FeatureIndex))

    def FeatureSet(self,populate='binary'):
        """ Make the FeatureSetMatrix """

        FeatureSetMatrix = num.zeros((self.nresponse,self.nfeatures))

        for iFeature in self.FeatureDict.keys():
            if self.SetType == 'training':
                TitleList = getTitlesByPart(self.FeatureDict[iFeature],self.yearDivide)
            else:
                TitleList = getTitlesByPartTest(self.FeatureDict[iFeature],self.yearDivide)

            for title in TitleList:
                iResponse = self.ReverseTitleDict[title]
                print title, iResponse
                if populate == 'binary':
                    FeatureSetMatrix[iResponse][iFeature] = 1.0
                elif populate == 'influence':
                    influence = getInfluenceByYearPart(self.FeatureDict[iFeature],\
                                self.YearDict[iResponse])
                    FeatureSetMatrix[iResponse][iFeature] = influence
                else:
                    print 'populate option not recognized'

        self.FeatureSetMatrix = FeatureSetMatrix


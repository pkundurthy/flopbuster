
import numpy as num
from flopbuster.readdb import getInfluenceHistory, getPartHistory
from flopbuster.misc import getYear


class person:

    def __init__(self, name):

        self.name = name
        self._get_history()

    def _get_history(self):

        # get release dates and Earnings factors from database
        self.ReleaseDates, self.EarningsFactor, MovieTitles = getInfluenceHistory(self.name)

        # make an array of only the years of release
        self.ReleaseYears = \
            [int(getYear(RDate.strftime("%Y-%m-%d"))) for RDate in self.ReleaseDates]

        # find the first and last years in which a release was made
        min_date = int(getYear(min(self.ReleaseDates).strftime("%Y-%m-%d")))
        max_date = int(getYear(max(self.ReleaseDates).strftime("%Y-%m-%d")))

        # make an evenly spaced array of years between 
        self.activeYears = num.arange(min_date,max_date,1)
        # the first active and last active year as attributes
        self.Date_of_FirstRelease = min_date
        self.Date_of_LastRelease = max_date

        # get the dictionary of various participations 
        # of given person
        partHist = getPartHistory(person)

        self.InfluenceMultiplier = InfluenceMultiplier(self.ReleaseDates,partHist)


    def computeInfluenceHistory(self,half_life=3.0):
        """ compute the Influence History """
        half_life = num.float(half_life)

        activeYearlyEarnings = \
            num.array([num.sum(self.EarningsFactor[num.where(self.ReleaseYears ==\
             yy)[0]]) for yy in self.activeYears])

        activeYearlyEarnings *= self.InfluenceMultiplier

        InfluenceFactor = []
        for i in xrange(len(self.activeYears)):
            if i == 0:
                decay = 1.0
                InfluenceFactor.append(activeYearlyEarnings[i])
            else:
                delta_time = self.activeYears[i]-self.activeYears[i-1]
                decay = (0.5)**(delta_time/half_life)
                InfluenceFactor.append(InfluenceFactor[-1]*decay + activeYearlyEarnings[i])

        self.InfluenceFactor = num.array(InfluenceFactor)

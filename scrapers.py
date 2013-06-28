
import re
import urllib2
import json
import csv
from BeautifulSoup import BeautifulSoup
import unicodedata

GoodKeyNames = [u'Plot', u'Rated', u'Title', u'Poster',\
                u'Writer', u'Response', u'Director', u'Released',\
                u'Actors', u'Year', u'Genre', u'Runtime', u'Type',\
                u'imdbRating', u'imdbVotes', u'imdbID']
BadKeyNames = [u'Response',u'Error']


def scrape_getthenumbers(outFile):
    """ a function that simply does a first order scraping 
        of the-numbers.com box office data
    """

    # record of all available box-office info
    BASE_URL = 'http://www.the-numbers.com/movies/records/allbudgets.php'

    # Soup the url and look for instances of tables
    soup = BeautifulSoup(urllib2.urlopen(BASE_URL))
    table = soup.find('table')
    
    # find the headers and remove blank unicode spaces
    hh = [header.text for header in table.findAll('th')]
    headers = []
    for el in hh: 
        headers.append(re.sub(u'&nbsp;',' ',el))

    head_line = ','.join(headers)

    # find the rows of data and generate writable csv lines
    rows = []
    for row in table.findAll('tr'):
        current_row_0 = [val.text.encode('utf8') for val in row.findAll('td')]
        current_row = []
        for i in range(len(current_row_0)):
            #skip the extra blank space column
            if i != 1:
                rr = current_row_0[i]
                #format the dollar entries to more number-ready form
                if i > 3: 
                    outstr = re.sub(u'&nbsp;',' ', rr)
                    outstr = re.sub(u'\$','',outstr)
                    outstr = re.sub(u',','',outstr)
                    current_row.append(outstr)
                else:
                    current_row.append(re.sub(u'&nbsp;',' ', rr))
        rows.append(current_row)

    out_file = open(outFile, 'w')
    print >> out_file, head_line

    # hard coding the row at which the movie table 
    # begins, on the web-page.
    start_row = 67
    lenght_array = []
    for i in range(len(rows)):
        # start creation of csv data
        if i >= start_row:
            lenght_array.append(len(rows[i]))
            print >> out_file, ','.join(rows[i])

    out_file.close()


def sqlready_csv(inFile,outFile):
    """ 
        creates an SQL read CSV file that can be loaded in to a database
    """

    fileData = open(inFile,'r').readlines()

    fileClean = open(outFile,'w')

    # counter that pads unknown Boolean elements with a string tag
    running_counter = 0

    for line in fileData:
        # going through the lines in first pull boxoffice csv
        line = line.strip('\n')
        splitMap = map(str, line.split(','))

        #default print output is True
        doPrint = True
        if splitMap[2] == ' ':
            running_counter += 1
            splitMap[i] = 'Unk'+str(running_counter).zfill(5)

        # skip movie is budget information is unavailable
        if splitMap[3] == ' ' or splitMap[3] == 'Unknown':
            doPrint = False

        # skip movie if box office intake is unavailable
        for i in [4,5]:
            if splitMap[i] == ' ' or splitMap[i] == 'Unknown':
                doPrint = False

        if doPrint: 
            lineOut = ','.join(splitMap)
            print >> fileClean, lineOut
    
    fileClean.close()


class ImdbAPIFunction:

    BASE_URL = 'http://www.omdbapi.com'

    def __init__(self, title,year=None):
        """ an instance of this object will scrape JSON like data from
        omdbapi.com for a given movie """

        self.title = title
        self.year = year
        self._process()
        self._cleandata()
        
    def _process(self):
        movie = re.sub(' ','+',self.title)
        try:
            movie = \
                unicodedata.normalize('NFKD', movie).encode('ascii','ignore')
        except:
            pass

        if self.year != None:
           url = "%s/?i=&t=%s&y=%s" % (self.BASE_URL, movie,self.year)
        else:
            url = "%s/?i=&t=%s" % (self.BASE_URL, movie)

        content = urllib2.urlopen(url).read()
        content = json.loads(content)
        self.data = content

    def _cleandata(self):

        newdata = {}
        NeedList = [u'Writer',u'Director',u'Actors',u'Genre']
        HaveList = self.data.keys()
        useList = list(set.intersection(set(NeedList),set(HaveList)))
        self.keylist = useList
        for key in useList:
            new_key = \
                unicodedata.normalize('NFKD', key).encode('ascii','ignore')
            new_dataform = unicodedata.normalize('NFKD',\
                                self.data[key]).encode('ascii','ignore')
            dSplit00 = map(str, new_dataform.split(', '))
            newdata[new_key] = dSplit00

        self.out = newdata


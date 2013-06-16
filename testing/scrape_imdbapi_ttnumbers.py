
import MySQLdb
import csv
import flopbuster
from matplotlib import pylab as plt
import numpy as num

title_List = flopbuster.readdb.getTitles_BoxOffice()
print len(title_List), len(set(title_List))

path_to_socket = '/var/mysql/mysql.sock'
db = MySQLdb.connect(host="localhost", user="root", passwd="",db='flopbuster',unix_socket=path_to_socket)
# db = MySQLdb.connect(host="localhost", user="root", passwd="",db='flopbuster')
cursor = db.cursor()

#Table Creation
cursor.execute("DROP TABLE IF EXISTS movie_meta;")
createStatement = "CREATE TABLE movie_meta"
createStatement += "(title VARCHAR(80),part VARCHAR(80), partType VARCHAR(25));"
cursor.execute(createStatement)

OutSQLFile = open('mysql_movie_meta.csv','w')

# for movie in ['Babylon A.D.','Bacheha-Ye aseman','Back to the Future']:
for movie in title_List:
    scraper = flopbuster.scrapers.ImdbAPIFunction(movie)
    #print scraper.data.keys()
    
    for key in scraper.keylist:
        title = movie
        typeKey = key
        for el in scraper.out[key]:
            part = el
            # print type(title),type(part), typeKey
            output_line = title+'|'+part+'|'+typeKey
            print output_line
            print >> OutSQLFile, output_line

OutSQLFile.close()

#loading data
loadStatement = 'LOAD DATA LOCAL INFILE "mysql_movie_meta.csv" INTO TABLE movie_meta'
loadStatement += ' FIELDS TERMINATED by "|" LINES TERMINATED BY "\\n"'
cursor.execute(loadStatement)
cursor.execute('CREATE INDEX id_index ON movie_meta(title)')



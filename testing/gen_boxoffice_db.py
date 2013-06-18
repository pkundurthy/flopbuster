


import MySQLdb
import csv
import flopbuster

path_to_socket = '/var/mysql/mysql.sock'
db = MySQLdb.connect(host="localhost", user="root", passwd="",db='flopbuster',unix_socket=path_to_socket)
# db = MySQLdb.connect(host="localhost", user="root", passwd="",db='flopbuster')
cursor = db.cursor()

#Table Creation
cursor.execute("DROP TABLE IF EXISTS boxoffice;")
createStatement = "CREATE TABLE boxoffice"
createStatement += "(released DATE,title VARCHAR(80),budget BIGINT,"
createStatement += "usgross BIGINT,worldgross BIGINT, totalgross BIGINT, MovieType VARCHAR(25) )"
cursor.execute(createStatement)

reader = csv.DictReader(open("../data_files/OutputPages01.csv", "rb"),delimiter=';')

OutMySql = open('mysql_boxoffice.csv','w')
for row in reader:

    reld = flopbuster.misc.date_to_mysqlDate(row['Released'])
    title = row['Movie']
    budget = row['Budget']
    usgross = row['US Gross']
    worldgross = row['Worldwide Gross']
    typeName = row['Type']

    totalgross = 0
    for el in [usgross,worldgross]:
        if el == '\N':
            el = 0
        else:
            el = int(el)
        totalgross += el

    totalgross = str(totalgross) 
    print reld,title,budget,usgross,worldgross,type
    line = reld+'|'+title+'|'+budget+'|'+\
           usgross+'|'+worldgross+'|'+totalgross+'|'+typeName
    print >> OutMySql, line

OutMySql.close()
#loading data
loadStatement = 'LOAD DATA LOCAL INFILE "mysql_boxoffice.csv" INTO TABLE boxoffice'
loadStatement += ' FIELDS TERMINATED by "|" LINES TERMINATED BY "\\n"'
cursor.execute(loadStatement)
cursor.execute('CREATE INDEX id_index ON boxoffice(title)')



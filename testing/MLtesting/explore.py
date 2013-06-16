

import MySQLdb
import flopbuster
from matplotlib import pylab as plt
import numpy as num

cursor = flopbuster.readdb.dbConnect()

statement1 = "select usgross,budget from boxoffice where (title in (select distinct title from movie_meta where (partType = 'Director' or partType = 'Genre')) and budget is not null and usgross is not null and released < '2006-12-31') order by released asc;"


cursor.execute(statement1)
result1 = cursor.fetchall()
x1g = num.array([x[0] for x in result1])
x1b = num.array([x[1] for x in result1])


statement2 = "select usgross,budget from boxoffice where (title in (select distinct title from movie_meta where (partType = 'Director' or partType = 'Genre')) and budget is not null and usgross is not null and released >= '2006-12-31') order by released asc;"

cursor.execute(statement2)
result2 = cursor.fetchall()
x2g = num.array([x[0] for x in result2])
x2b = num.array([x[1] for x in result2])

# plt.plot(result1,'b.')

print min(x1g-x1b), max(x1g-x1b), num.median(x1g-x1b)
fig = plt.subplot(111)
plt.hist( (x1g-x1b))

plt.show()


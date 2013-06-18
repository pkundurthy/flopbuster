

import flopbuster
from matplotlib import pylab as plt
import numpy as num

cursor = flopbuster.readdb.dbConnect()

statement1 = 'select title, ifnull(totalgross,0), ifnull(usgross,0),'
statement1 += ' ifnull(worldgross,0), ifnull(budget,0) from boxoffice;'

cursor.execute(statement1)
results = cursor.fetchall()

titles = [x[0] for x in results]
tgross = num.array([x[1] for x in results])
usgross = num.array([x[2] for x in results])
wgross= num.array([x[3] for x in results])
budget = num.array([x[4] for x in results])

plt.hist(tgross-budget)
print len(num.where(tgross-budget <= 0)[0])
print len(tgross)


# plt.show()
# plt.hist(usgross-budget)
# plt.show()

# plt.hist(wgross-budget)
# plt.show()




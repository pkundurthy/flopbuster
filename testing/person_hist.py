
import flopbuster
from matplotlib import pylab as plt
import numpy as num

plist = ['James Cameron','Steven Spielberg','J.J. Abrams','George Lucas']

clist = ['b','r','g','c','k','y']

"""
for person in plist:
    d,suc = flopbuster.discovery.getInfluenceHistory(person)
    plt.plot(d,suc)
    plt.plot(d,suc,'o',color=clist.pop())

plt.show()
"""


rel,gross = flopbuster.discovery.getAllGrossFactor()
print '> 100 ',len(num.where(gross > 100)[0])
print '10 - 100 ',len(num.where( (gross > 10) & (gross < 100) )[0])
print '1 - 10',len(num.where( (gross > 5) & (gross < 10) )[0])
print '2 - 5 ',len(num.where( (gross > 2) & (gross < 5)) [0])
print '0 - 2 ',len(num.where( (gross > 0) & (gross < 2)) [0])

budget,totalgross = flopbuster.discovery.getInOutMoney()


plt.plot(budget,totalgross,'b.')
plt.yscale('log')
plt.xscale('log')
plt.show()

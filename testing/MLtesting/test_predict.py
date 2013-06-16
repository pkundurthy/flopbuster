
import cPickle
import sys
import numpy as num
from matplotlib import pylab as plt


metric_test_file = open('MetricFile_Test.pickle',"rb")
metric_test = cPickle.load(metric_test_file)

predict_test_file = open('PredictFile.pickle',"rb")
predict_test = cPickle.load(predict_test_file)

# plt.plot(predict_test,metric_test,'b.')
# plt.show()

# plt.hist(predict_test,color='g')
# plt.hist(metric_test,color='b')
# plt.show()

total = 0
match = 0

print len(num.where((predict_test-metric_test) == 0)[0])


for i in range(len(predict_test)):
    print i,',',predict_test[i],',', metric_test[i],','
    total += 1
    if predict_test[i] == metric_test[i]:
        match += 1

print match,',', total,',', float(match)/float(total)


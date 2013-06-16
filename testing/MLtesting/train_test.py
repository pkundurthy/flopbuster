

from sklearn.ensemble import RandomForestClassifier
import scipy
import cPickle
from matplotlib import pylab as plt


train_file = open('TrainFile.pickle',"rb")
train = cPickle.load(train_file)

metric_train_file = open('MetricFile_Train.pickle',"rb")
metric_train = cPickle.load(metric_train_file)

test_file = open('TestFile.pickle',"rb")
test = cPickle.load(test_file)

metric_test_file = open('MetricFile_Test.pickle',"rb")
metric_test = cPickle.load(metric_test_file)


rf = RandomForestClassifier(n_estimators=200, \
                            min_samples_split=2, n_jobs=-1)

print 'fitting the model'
rf.fit(train, metric_train)
print 'making predictions'
predicted_metric = rf.predict(test)


predict_file = open('PredictFile.pickle',"wb")
cPickle.dump(predicted_metric, predict_file, protocol=2)




from dataset import getSymbolCSV, getPrices, getFeatureVector,\
                    labelExamples, trainClassifier, historyCheck

train_data_path = 'vol_100_train.csv'
test_data_path = 'vol_100_test.csv'

dataFrame = getSymbolCSV(train_data_path)
open, high, low, close = getPrices(dataFrame)

classifier = trainClassifier(*labelExamples(open, high, low, close))

historyCheck(test_data_path, classifier, getFeatureVector)

''' OUTPUT:

Data length: 8019 

Labeled 1: 3494
Labeled -1: 3523
Labeled zero: 887

Time: 1.4929649829864502

Score: 0.4354974704890388

Predictions: Counter({-1: 1329, 1: 922, 0: 121})
Data length: 1227 


History check:
Trades: 1070
Plus: 587
Minus: 483
Win: 0.549

Modelling balance:

USD: 1678.9938838777957
Max loss series: 7
Min balance: 860.3210944218771

'''

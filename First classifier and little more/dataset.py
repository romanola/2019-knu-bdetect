import pandas as pd
import time
import csv
from collections import Counter
from indicator import *

from sklearn import svm, neighbors
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split

def getSymbolExcel(path):
    """
    if you keep data in excel, you can open it as DataFrame object
    :param path: path of your excel file
    :return: DataFrame object
    """

    return pd.read_excel(path)

def getSymbolCSV(path):
    """
    if you keep data in csv, you can open it as DataFrame object
    :param path: path of your excel file
    :return: DataFrame object
    """

    return pd.read_csv(path)

def getSymbolHtml(path):
    """
    if you keep data as html table, you can open it as DataFrame object
    :param symbol: symbol if it's in existing data
    :param path: path of your excel file
    :return: DataFrame object
    """

    return pd.read_html(path, parse_dates=True)

def mt4ToCSV(path, newfilename = None):
    '''
    If you exported candles to csv from MetaTrader 4 or 5,
    you can convert it to csv with commas to easily open it as DataFrame object.
    :param path: path to your file
    :param newfilename: name of creating file
    :return: None
    '''
    data = [['DATE','TIME','OPEN','HIGH','LOW','CLOSE','TICKVOL','VOL','SPREAD']]

    file = open(path,'r')

    lines = file.readlines()
    for l in range(1,len(lines)):
        data.append(list(lines[l].split()))

    print(len(data))
    writeCSV(data, newfilename if not newfilename is None else 'newCsvFile.csv')

def writeCSV(data, filename):
    with open(filename, 'w', newline='') as file:
        wrt = csv.writer(file)
        wrt.writerows(data)

def getPrices(data):
    '''
    Get prices data as np arrays. np arrays are more than 10x faster!
    :param data: DataFrame with prices of candles
    :return: open, high, low, close prices as np.array 's
    '''
    close = np.array(data['CLOSE'][:])
    open = np.array(data['OPEN'][:])
    high = np.array(data['HIGH'][:])
    low = np.array(data['LOW'][:])

    print('Data length:',len(close),'\n')

    return open, high, low, close

def getFeatureVector(open, high, low, close, ind):
    x0 = atr(close=close, high=high, low=low, period=20, ind=ind)/\
         atr(close=close, high=high, low=low, period=100, ind=ind)
    x1 = momentum(close, period=14, curInd=ind)
    x2 = trendDeviation(close, 15, ind)
    x3 = acp(close, 5, 12, ind)
    x4 = sma(close, 30, ind-11)
    x5 = sma(close, 10, ind-4)

    return [1, x0, x1, x2, x3, close[ind]/x5, x4/x5]

def labelExamples(open, high, low, close):
    '''
    Labeling your data
    1 - BUY
    -1 - SELL
    0 - hold
    :param open: open prices
    :param high: high prices
    :param low: low prices
    :param close: close prices
    :return: two lists: feature vectors and class these vectors belongs to
    '''

    labeledUp = 0
    labeledDown = 0
    labeledZero = 0

    featureData = []
    target = []

    offset = 105
    estimate = 0.15

    for ind in range(offset,len(close)-10):

        _change = change(open[ind+1],close[ind+1])*100
        fv = getFeatureVector(open, high, low, close, ind)
        featureData.append(fv)

        if _change >= estimate:
            target.append(1)
            labeledUp+=1
        elif _change <= -estimate:
            target.append(-1)
            labeledDown+=1
        else:
            target.append(0)
            labeledZero+=1

    print('Labeled 1:',labeledUp)
    print('Labeled -1:',labeledDown)
    print('Labeled zero:',labeledZero)
    return featureData, target

def trainClassifier(featureData, target):
    '''
    Train classifier using VotingClassifier with LinearSVC, RandomForestClassifier,
    KNeighborsClassifier, DecisionTreeClassifier algorithms
    :param featureData: feature vector
    :param target: class feature vector belongs to
    :return: classifier
    '''

    toLearn = 0.7
    trainFeature, testFeature, trainTarget, testTarget = train_test_split(featureData, target, test_size=1 - toLearn)

    clf = VotingClassifier([('lcsv', svm.LinearSVC(max_iter=1000)),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor',RandomForestClassifier()),
                            ('dtree',DecisionTreeClassifier())])

    t1 = time.time()
    clf.fit(trainFeature, trainTarget)
    print('Time:',time.time()-t1)
    print()

    winRate = clf.score(testFeature, testTarget)
    print('Score:',winRate)
    print()

    predictions = clf.predict(testFeature)
    print('Predictions:',Counter(predictions))

    return clf

def historyCheck(path, classifier, getFeatureVector):
    '''
    Test your classifier on historical data.
    Also modeling your account balance if you are using Martingale system.
    Balance starts with 1000 USD and will be top up after your classifier epic fail :)

    :param path: path to csv file with your data
    :param classifier:
    :param getFeatureVector: function to get feature vector of data
    :return: None
    '''
    data = getSymbolCSV(path=path)

    open, high, low, close = getPrices(data)

    offset = 105

    trades = 0
    plus = 0
    minus = 0

    start = offset
    finish = len(close)-10

    WinLoss = []

    for i in range(start,finish):
        try: # smth wrong happens here. it's ok
            pred = classifier.predict([getFeatureVector(open, high, low, close, i)])[0]
        except Exception as ex:
            print(ex)
            break

        if pred == 1:
            trades+=1
            if close[i+1]>open[i+1]:
                plus+=1
                WinLoss.append(1)
            else:
                minus+=1
                WinLoss.append(0)


        if pred == -1:
            trades+=1


            if close[i+1]<open[i+1]:
                plus+=1
                WinLoss.append(1)
            else:
                minus+=1
                WinLoss.append(0)

    print('\nHistory check:')
    print('Trades:',trades)
    print('Plus:',plus)
    print('Minus:',minus)
    print('Win:',0 if trades==0 else round(plus/trades,3))
    print()

    print('Modelling balance:')

    MaxSeries = 0
    CurSer = 0

    init_bal = 1000
    initial_stake = 1
    stake = 1
    USD = init_bal
    min_balance = USD

    for i in WinLoss:
        USD -= stake

        if i == 1:
            USD += stake*1.94
            stake = initial_stake
            CurSer = 0
        else:
            stake *= 2.15
            CurSer+=1

        MaxSeries = max(MaxSeries,CurSer)
        min_balance = min(min_balance, USD)

        if USD<=stake:
            print('BALANCE OUT!!!',USD,stake)
            stake = initial_stake
            USD = init_bal


    MaxSeries = max(MaxSeries,CurSer)
    min_balance = min(min_balance, USD)

    print()
    print('USD:',USD)
    print('Max loss series:',MaxSeries)
    print('Min balance:',min_balance)

if __name__=='__main__':
    mt4ToCSV('vol_100_mt4_tr.csv','vol_100_train.csv')
    mt4ToCSV('vol_100_mt4_test.csv','vol_100_test.csv')

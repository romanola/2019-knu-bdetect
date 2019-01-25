"""
This module is aimed on organizing log data both from Game and Touch event.

These functions will help you to work with csv files:
    - writeCSV(data, filename)
    - prepareGameLogFile(path, save = False)
    - prepareTouchLogFile(path, save = False)
    - openGameLog(path)
    - openTouchLog(path)
    - defineLogType(path = None, dataFrame = None) # needs to be corrected

All the data will be split on blocks. Each block is described by class Block.

Split data from your files on Blocks and then on train and test data using splitData function:
    - splitData(botTouch, botGame, humanTouch, humanGame, timeFrame, testSize)

it is not ideal working module and obviously it is not the best organisation of datasets.
Anyway, feel free to clarify any moment!
"""

import random
import pandas as pd
import numpy as np
import csv

GAME_LOG_KEYS = ['Time','Event','X','Y']
TOUCH_LOG_KEYS = ['Timestamp','ms','touch-event','X','Y','major','minor']


def writeCSV(data, filename):
    with open(filename, 'w', newline='') as file:
        wrt = csv.writer(file)
        wrt.writerows(data)

def prepareGameLogFile(path, save = False):
    '''
    Prepares log file to comfortable using:
    1. Convert to int time value
    2. Remove spaces in the start and end of string of event type
    3. Convert to float X and Y coordinates
    :param path: path to log .csv file
    :param save: optional parameter defines to save or not prepared data
    :return: DataFrame object with prepared data
    '''
    data = pd.read_csv(path)
    new_data = data.values.transpose()

    def toInt(x):
        try:
            return int(x)
        except:
            return None

    def Strip(x:str):
        return x.strip()

    def toFloat(x):
        try:
            return float(x)
        except:
            return None

    transform = [np.vectorize(toInt), np.vectorize(Strip), np.vectorize(toFloat), np.vectorize(toFloat)]

    for i in range(new_data.shape[0]):
        try:
            new_data[i] = transform[i](new_data[i])
        except:
            print(new_data[i])
            raise  Exception
    new_data = new_data.transpose()

    if save:
        writeCSV(new_data, 'prepared_'+path)

    return pd.DataFrame(new_data)

def prepareTouchLogFile(path, save = False):
    '''
    Prepares log file to comfortable using:
    1. Convert to int timestamp, ms and touch_event
    2.Convert to float X,Y coordinates and contacts major, minor
    :param path: path to file
    :param save: option whether you want to save prepared data
    :return: DataFrame object with prepared data
    '''
    data = pd.read_csv(path)
    new_data = data.values.transpose()

    def toInt(x):
        try:
            # 1.0 fails to convert to int, so we have to make some operations
            return int(x[:x.find('.')]) if '.' in x else int(x)
        except:
            return None

    def toFloat(x):
        try:
            return float(x)
        except:
            return None

    transform = [np.vectorize(toInt)]*3 + [np.vectorize(toFloat)]*4

    for i in range(new_data.shape[0]):
        new_data[i] = transform[i](new_data[i])

    new_data = new_data.transpose()

    if save:
        writeCSV(new_data, 'prepared_'+path)

    return pd.DataFrame(new_data)

def openGameLog(path):
    '''
    Opens .csv file with Game Log of EjikAdventures
    :param path: path to file
    :return: DataFrame object
    '''
    return pd.read_csv(path, names=GAME_LOG_KEYS)

def openTouchLog(path):
    '''
    Opens .csv file with Touch Log of EjikAdventures
    :param path: path to the file
    :return: DataFrame object
    '''
    return pd.read_csv(path, names=TOUCH_LOG_KEYS)

def defineLogType(path = None, dataFrame = None):
    ''' TODO: FIX INCORRECT DEFINE OF TOUCH
    Defines what type this log is: Touch or Game.
    Takes path to file or DataFrame object if file is already opened
    :param path: path to file
    :param dataFrame: DataFrame object if file is already opened
    :return: 'Game' or 'Touch' or None if type is undefined
    '''

    if not dataFrame and not path: return None

    if not dataFrame:
        dataFrame = pd.read_csv(path)

    gameCondition = [lambda x0: type(x0) == int or type(x0) == np.float64,
                     lambda x1: x1 in {'Touch','Drop','Fight'},
                     lambda x2: type(x2) == float or pd.isna(x2),
                     lambda x3: type(x3) == float or pd.isna(x3)] # may be missed data somewhere

    touchCondition = [lambda x0: x0>1500000000,
                      lambda x1: 0<=x1<=1000,
                      lambda x2: x2 in {0,1,2},
                      lambda x3: True or type(x3) == float,
                      lambda x4: True or type(x4) == float,
                      lambda x5: True or type(x5) == float,
                      lambda x6: True or type(x6) == float]

    values = dataFrame.values.transpose() # - np.array of np.array or matrix of values

    if values.shape[0] == 4: # it is probably Game
        row = 0
        for condition in gameCondition:
            if False in np.vectorize(condition)(values[row]):
                return None
            row+=1
        return 'Game'

    if values.shape[0] == 7: # it is probably Touch
        row = 0
        for condition in touchCondition:
            if False in np.vectorize(condition)(values[row]):
                return None
            row+=1
        return 'Touch'

def splitData(botTouch, botGame, humanTouch, humanGame, timeFrame, testSize):
    '''
    Split your data on Train and Test.
    Before that your data will be split on pieces(blocks) defined by timeFrame

    :param botTouch: DataFrame object which relates to bot's Touch log
    :param botGame: DataFrame object which relates to bot's Game log
    :param humanTouch: DataFrame object which relates to human's Touch log
    :param humanGame: DataFrame object which relates to human's Game log
    :param timeFrame: the difference between every time of event in block will be less than timeFrame, sec
    :param testSize: the share of testSize where 1 is 100% of data length. testSize+trainSize = 1
    :return: two dict"s: dict for Train and Test.
             keys are 'bot' and 'human' and value of each is list of blocks
    '''
    botBlocks = []
    humanBlocks = []

    def splitBlocks(touch, game):
        blocks = []

        rowT = 0
        rowG = 0
        curBlock = Block()

        x,y = 0,0
        while game['Event'][rowG] != 'Touch':
            rowG += 1
            x,y = game['X'][rowG], game['Y'][rowG]

        while (touch['X'][rowT], touch['Y'][rowT]) != (x,y):
            rowT+=1

        while rowT<touch.values.shape[1] and rowG<game.values.shape[1]:
            if game['Event'] == 'Touch':
                while rowT<touch.values.shape[1]:
                    curBlock.touch(touch['Timestamp'][rowT]*1000+touch['ms'][rowT],
                                   touch['X'][rowT], touch['Y'][rowT],
                                   touch['touch-event'][rowT], touch['major'][rowT], touch['minor'][rowT])

                    if touch['touch-event'][rowT] == 0:
                        rowT+=1
                        break
                    rowT+=1
                rowG+=1
            elif game['Event'] == 'Drop':
                curBlock.drop(game['Time'][rowG]-game['Time'][rowG-1], game['X'][rowG])
                rowG+=1
            elif game['Event'] == 'Fight':
                curBlock.fight(game['Time'][rowG]-game['Time'][rowG-1], game['X'][rowG])
                rowG+=1

            if curBlock.timeFrame()>timeFrame:
                blocks.append(curBlock)
                curBlock = Block()

        return blocks


    botBlocks = splitBlocks(botTouch, botGame)
    humanBlocks = splitBlocks(humanTouch, humanGame)


    random.shuffle(botBlocks)
    random.shuffle(humanBlocks)

    indexBot = int(len(botBlocks)*(1-testSize))
    indexHuman = int(len(humanBlocks)*(1-testSize))

    return {'bot':botBlocks[:indexBot], 'human':humanBlocks[:indexHuman]},\
           {'bot':botBlocks[indexBot+1:], 'human':humanBlocks[indexHuman+1:]}

class Block:
    def __init__(self, startTime = 0):
        self.start = startTime
        self.finish = startTime
        self.fights = 0
        self.drops = 0
        self.touches = 0
        self.events = []

    def touch(self, time, x, y, type, major, minor):
        self.events.append(('Touch', time, x, y, type, major, minor))
        self.touches+=1
        self.finish = time

    def drop(self, time, balanceAfter):
        self.drops+=1
        self.finish += time
        self.events.append(('Drop',self.finish, balanceAfter))

    def fight(self, time, expAfter):
        self.fights+=1
        self.finish += time
        self.events.append(('Fight',self.finish,expAfter))

    def timeFrame(self):
        return self.finish - self.start


if __name__ == '__main__':
    def test1():
        pg = 'log_human_Game.csv'
        pt = 'log_human_Touch.csv'

        gameLog = prepareGameLogFile(pg, True)
        touchLog = prepareTouchLogFile(pt, True)

        print(defineLogType(pg))
        print(defineLogType(pt))

        print(defineLogType('prepared_'+pg))
        print(defineLogType('prepared_'+pt))


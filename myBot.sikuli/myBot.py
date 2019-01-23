import random as rd
import math
import time


def startGame():
    if exists(Pattern("newGame-1.png").similar(0.38)):
        click("newGame-2.png")
    else:
        popup("Can't start new game. Are you on main title screen?")


def getDelay():
    delay = 0
    tmp = rd.randrange(20)
    if not tmp % 6:
        delay = rd.randrange(2, 5)
    else:
        delay = rd.randrange(2)
    return delay


def getMouseCoordinates():
    mouse = Env.getMouseLocation()
    return mouse.getX(), mouse.getY()


def getHeroLocation():
    x = 793
    y = 364
    return x, y

def getRegion():
    a = (144, 339)
    b = (144, 46)
    c = (753, 46)
    d = (753, 339)
    return a, b, c, d

def getRandomAngle():
    angle = rd.randrange(10000)
    return angle % 360

def findAllBitcoins():
    bitcoins = findAll(Pattern("bitcoin-1.png").similar(0.38))
    bitList = []
    for i in bitcoins:
        bitList.append((i.getX(), i.getY()))
    return bitList


def findAllMonsters():
    monsters = findAll(Pattern("monster.png").similar(0.20))
    monsterList = []
    for i in monsters:
        monsterList.append((i.getX(), i.getY()))
    return monsterList

def check():
    return findAllBitcoins() != [] or findAllMonsters() != []


def findBestMove():
    x0, y0 = getHeroLocation()
    items = findAllBitcoins() + findAllMonsters()
    items.sort(key=lambda x: math.sqrt((x0 - x[0])**2 + (y0 - x[1])**2))
    return items[0]

def findRandomMove():
    click(Location(rd.randrange(200), rd.randrange(200)))


def move():
    if check():
        click(Location(*findBestMove()))
    else:
        findRandomMove()
         
def main():
    #startGame()
    while True:
        move()
        time.sleep(getDelay())


def test():
    icons = findAll(Pattern("bitcoin.png").similar(0.33))
    return icons


if __name__ == '__main__':
    main()

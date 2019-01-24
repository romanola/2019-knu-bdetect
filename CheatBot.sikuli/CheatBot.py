import random
import math

EJIK_NOT_FOUND = "Ejik not found. Are you running the game?"

AHEAD = "N"
AHEAD_STARBOARD = "NE"
STARBOARD = "E"
AFT_STARBOARD = "SE"
AFT = "S"
AFT_PORT = "SW"
PORT = "W"
AHEAD_PORT = "NW"

DELAY_FACTOR = 400

scr = Screen.getBounds(0)
# SCREEN_RES_X = 1080
# SCREEN_RES_Y = 2220 
SCREEN_RES_X = scr.height
SCREEN_RES_Y = scr.width

def StartNewGame():
    wait(Pattern("1548085274534.png").exact(), 120)
    if exists(Pattern("1548085274534.png").exact()):
        click(Pattern("1548085274534.png").exact())
    else:
        popup("Can't start new game. Are you on main title screen?")
    
def DoNothing():
    print("!!!!!")

def GetMouseCoordinates():
    getmouseLoc = Env.getMouseLocation()
    x = getmouseLoc.getX()
    y = getmouseLoc.getY()
    return x, y

def GetDelay(x, y):
    hipotenuse = math.sqrt(math.pow(x - (SCREEN_RES_X / 2) , 2) + math.pow(y - (SCREEN_RES_Y / 2) , 2))
    ReturnDelay = hipotenuse / DELAY_FACTOR
    if ReturnDelay < 0:
        return 0
    else:
        return(ReturnDelay) 

def EatApple(delay):
        try:
            click(Pattern("1548242462659.png").similar(0.75))

        except:
            EatMushroom(delay)
            return
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))


def EatMushroom(delay):
        try:
            click(Pattern("1548242547155.png").similar(0.50))
        except: 
            EatApple(delay)
            return
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))

        


def RunN(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-834,33), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-834,33)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-834,33))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else:
        popup(EJIK_NOT_FOUND)

def RunNE(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-201,60), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-201,60)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-201,60))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def RunE(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def RunSE(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-364,666), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def RunS(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-846,657), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def RunSW(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-1494,635), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def RunW(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-1512,355), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def RunNW(delay):
    wait(Pattern("1548085434717.png").similar(0.55).targetOffset(-1427,52), delay)
    if exists(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339)):
        click(Pattern("1548085434717.png").similar(0.55).targetOffset(-205,339))
        x, y = GetMouseCoordinates()
        wait(GetDelay(x, y))
    else: 
        popup(EJIK_NOT_FOUND)

def Run(direction, delay):
    if direction == AHEAD:
        RunN(delay)
        
    elif direction == AHEAD_STARBOARD:
        RunNW(delay)

    elif direction == STARBOARD:
        RunE(delay)
        
    elif direction == AFT_STARBOARD:
        RunSE(delay)
        
    elif direction == AFT:    
        RunS(delay)
        
    elif direction == AFT_PORT:
        RunSW(delay)
        
    elif direction == PORT:
        RunW(delay)
        
    elif direction == AHEAD_PORT:                
        RunNW(delay)
    else: 
        RunSW(delay)
        
def RandomRun(delay):
   Direction = [AHEAD, AHEAD_STARBOARD, AFT_STARBOARD, AFT, AFT_PORT, PORT, AHEAD_PORT]
   Run(random.choice(Direction), delay)

def RandomRun_new:
    """
       TODO finish this
    """
    center_x = SCREEN_RES_X // 2
    center_y = SCREEN_RES_Y // 2
    diag = math.sqrt(math.pow(center_x , 2) + math.pow(center_y, 2))
    radius = diag // 5
    radius += (random.random() - 0.5) * (radius // 2)
    degree = random.choice(list(range(360)))
    
    
#StartNewGame()

while(1):
   
    Action = ['apple' , 'mushroom']
    res = random.choice(Action)
    print (res + " rolled")
    if res == 'apple':
        go = exists(Pattern("1548242462659.png").similar(0.85), 1)
        if go !=  None:
            print ("Found apple, clicking")
            EatApple(1)
        else:
             go = exists(Pattern("1548242547155.png").similar(0.50), 1)  
             if go !=  None:
                 print ("Found mushroom, clicking")
                 EatMushroom(1)
             else:
                 print ("Nothing found, running")
                 RandomRun(1)
            
    else:
        go = exists(Pattern("1548242547155.png").similar(0.50), 1)
        if go !=  None:
            print ("Found mushroom, clicking")
            EatMushroom(1)
        else:
             go = exists(Pattern("1548242462659.png").similar(0.85), 1)  
             if go !=  None:
                 print ("Found apple, clicking")
                 EatApple(1)
             else:
                 print ("Nothing found, running")
                 RandomRun(1)
            
    

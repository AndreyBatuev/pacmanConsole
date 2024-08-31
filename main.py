import enum
import os
import sys
import keyboard
import time
import random
from termcolor import colored

gameSpeed = 0.2
errMsg = ""
lastPacmanCord = 0
pacmanCord = 0
lenMap = 0
score = 0
class turnPacman(enum.Enum):
    left = 0
    right = 1
    down = 2
    up = 3
    no = 4

class colorTerm(enum.Enum):
    red = 0
    green = 1
    yellow = 2
    blue = 3
    magenta = 4
    cyan = 5
    white = 6
    light_grey = 7
    light_red = 8
    light_green = 9
    light_yellow = 10
    default = 11
    no = 12
def colorPrint(string = "", color = colorTerm.no):
    if color == colorTerm.red:
        sys.stdout.write(colored(string, 'black', 'on_red'))
    elif color == colorTerm.green:
        sys.stdout.write(colored(string, 'black', 'on_green'))
    elif color == colorTerm.yellow:
        sys.stdout.write(colored(string, 'black', 'on_yellow'))
    elif color == colorTerm.blue:
        sys.stdout.write(colored(string, 'black', 'on_blue'))
    elif color == colorTerm.magenta:
        sys.stdout.write(colored(string, 'black', 'on_magenta'))
    elif color == colorTerm.cyan:
        sys.stdout.write(colored(string, 'black', 'on_cyan'))
    elif color == colorTerm.white:
        sys.stdout.write(colored(string, 'black', 'on_white'))
    elif color == colorTerm.light_grey:
        sys.stdout.write(colored(string, 'black', 'on_light_grey'))
    elif color == colorTerm.light_red:
        sys.stdout.write(colored(string, 'black', 'on_light_red'))
    elif color == colorTerm.light_green:
        sys.stdout.write(colored(string, 'black', 'on_light_green'))
    elif color == colorTerm.light_yellow:
        sys.stdout.write(colored(string, 'black', 'on_light_yellow'))
    elif color == colorTerm.default:
        sys.stdout.write(string)
    else:
        global FatalError
        global errMsg
        FatalError = True
        errMsg = "Incorrect color - " + str(color)
        fatalOut()

tPacman = turnPacman.no
FatalError = False
scoresExists = True
teleport1Cord = 0
teleport2Cord = 0 


scoresCords = []
gameOver = False
gameWin = False
tileMap = [ "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "n", 
            "#", "#", " s", " s", " s", " s", " s", " s", "#", " s", " s", " s", " s", " s", " s", "#", "#", "n", 
            "#", "#", " s", "#", " s", "#", "#", " s", "#", " s", "#", "#", " s", "#", " s", "#", "#", "n", 
            "#", "#", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", "#", "#", "n", 
            "#", "#", " s", "#", " s", "#", " s", "#", "#", "#", " s", "#", " s", "#", " s", "#", "#", "n", 
            "#", "#", " s", " s", " s", "#", " s", " s", "#", " s", " s", "#", " s", " s", " s", "#", "#", "n", 
            "#", "#", "#", " s", " s", "#", "#", " s", " s", " s", "#", "#", " s", " s", "#", "#", "#", "n", 
            "#", "#", "#", " s", " s", "#", " s", " s", " s", " s", " s", "#", " s", " s", "#", "#", "#", "n", 
            "#", "t", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", "t", "#", "n", 
            "#", "#", "#", " s", " s", "#", " s", " s", " s", " s", " s", "#", " s", " s", "#", "#", "#", "n", 
            "#", "#", "#", " s", " s", "#", " s", "#", "#", "#", " s", "#", " s", " s", "#", "#", "#", "n", 
            "#", "#", " s", " s", " s", " s", " s", " s", "#", " s", " s", " s", " s", " s", " s", "#", "#", "n", 
            "#", "#", " s", "#", " s", "#", "#", " s", "#", " s", "#", "#", " s", "#", " s", "#", "#", "n", 
            "#", "#", "©", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", "#", "#", "n", 
            "#", "#", "#", " s", " s", " s", " s", "#", "#", "#", " s", " s", " s", " s", "#", "#", "#", "n", 
            "#", "#", " s", " s", " s", "#", " s", " s", " s", " s", " s", "#", " s", " s", " s", "#", "#", "n", 
            "#", "#", " s", "#", "#", "#", "#", " s", "#", " s", "#", "#", "#", "#", " s", "#", "#", "n", 
            "#", "#", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", " s", "#", "#", "n", 
            

            "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "n",
            "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "n",  
            "#", "#", "#", "SCORE", "#",   "n",   
            "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "n",  
            "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "n",  
            "k", "#", "#", "teleport1Cord", "#", "#", "#", "#", "#", "#", "k", "n",   
            "k", "#", "#", "teleport2Cord", "#", "#", "#", "#", "#", "#", "k", "n",   
            "k", "#", "#", "pacmanCord",  "#", "#", "#", "#", "#", "#", "k", "n",   
            "k", "#", "#", "lastPacmanCord", "#", "#", "#", "#", "#","#", "k", "n",   
              ]
        # 'l' - last \n
        # 'k' edge of the field
        # '#' wall
        # ' ' empty space
        # '©' pacman
        # 'SCORE' score count
        # ' s' score and empty space
        # 't' portal

winScreen =  "#################"

allGhostsNames = []
class Ghost:
    color = colorTerm.no
    handicapNow = 0
    def __init__(self, name , ghostColor, startCord, algo):
        global lastCord
        global cord 
        global color
        self.color = ghostColor
        ghostTurn = turnPacman.no
        self.name = name
        global allGhostsNames
        allGhostsNames.append(self.name)
        self.lastCord = startCord
        self.cord = startCord
        
        self.algo = algo
    def existsName(symbol):
        for i in range(len(allGhostsNames)):
            if symbol == i:
                return True
        return False
            
    def goTo(self, turn = turnPacman.no):
        global tileMap
        global teleport1Cord
        global teleport2Cord
        Ghost.ghostTurn = turn
        if turn == turnPacman.left and self.handicapNow >= 6:
            self.lastCord = self.cord
            if tileMap[self.cord - 1] == 't':
                if self.cord - 1 == teleport1Cord:
                    self.cord = teleport2Cord
                    tileMap[self.cord + 1] = Ghost.__name__
                    tileMap[self.lastCord] = " "
                    
                    Ghost.ghostTurn = turnPacman.left
            if tileMap[self.cord - 1] != '#' :
                self.cord = self.cord - 1
                tileMap[self.lastCord] = " "
                tileMap[self.cord] = Ghost.__name__
            self.handicapNow = 0
        elif turn == turnPacman.right and self.handicapNow >= 6:
            self.lastCord = self.cord
            if tileMap[self.cord + 1] == 't':
                if self.cord + 1 == teleport2Cord:
                    self.cord = teleport1Cord
                    tileMap[self.cord + 1] = Ghost.__name__
                    tileMap[self.lastCord] = " "
                    Ghost.ghostTurn = turnPacman.right
            if tileMap[self.cord + 1] != '#'  :
                self.cord = self.cord + 1
                tileMap[self.lastCord] = " "
                tileMap[self.cord] = Ghost.__name__
            self.handicapNow = 0
        elif turn == turnPacman.up and self.handicapNow >= 6:
            self.lastCord = self.cord
            if tileMap[self.cord - lenMap] != '#' :
                self.cord = self.cord - lenMap
                tileMap[self.lastCord] = " "
                tileMap[self.cord] = Ghost.__name__
                Ghost.ghostTurn = turnPacman.up
            self.handicapNow = 0
        elif turn == turnPacman.down and self.handicapNow >= 6:
            self.lastCord = self.cord
            if tileMap[self.cord + lenMap] != '#' :
                self.cord = self.cord + lenMap
                tileMap[self.lastCord] = " "
                tileMap[self.cord] = Ghost.__name__
                Ghost.ghostTurn = turnPacman.down
            self.handicapNow = 0
        self.handicapNow += 1
    def thinkWay(self):
        turn = self.algo()
        return turn

def pinkiAlgo():
    direction = random.choice([turnPacman.down,turnPacman.left,turnPacman.right,turnPacman.up])
    return direction

#Blinky = Ghost("b", 13, pinkiAlgo)
Pinki = Ghost("p", colorTerm.red, 152, pinkiAlgo)
#Inky = Ghost("b", 13, pinkiAlgo)
#Clyde = Ghost("b", 13, pinkiAlgo)

def draw():
    global FatalError
    global tPacman
    global lastPacmanCord 
    global pacmanCord
    global lenMap
    global score
    global scoresExists
    global gameOver

    global Pinki

    
    if tPacman == turnPacman.left:
        lastPacmanCord = pacmanCord
        if tileMap[pacmanCord - 1] == ' s':
            score += 1
        if tileMap[pacmanCord - 1] == 't':
            
            if pacmanCord - 1 == teleport1Cord:
                pacmanCord = teleport2Cord
                tileMap[pacmanCord + 1] = "©"
                tileMap[lastPacmanCord] = " "
                
                tPacman = turnPacman.left
        if tileMap[pacmanCord - 1] != '#':
            pacmanCord = pacmanCord - 1
            tileMap[lastPacmanCord] = " "
            tileMap[pacmanCord] = "©"
        if Pinki.cord == pacmanCord:
            gameOver = True
    elif tPacman == turnPacman.right:
        lastPacmanCord = pacmanCord
        if tileMap[pacmanCord + 1] == 't':
            
            if pacmanCord + 1 == teleport2Cord:
                pacmanCord = teleport1Cord
                tileMap[pacmanCord + 1] = "©"
                tileMap[lastPacmanCord] = " "
                
                tPacman = turnPacman.right

        if tileMap[pacmanCord + 1] == ' s':
            score += 1
        if tileMap[pacmanCord + 1] != '#':
            pacmanCord = pacmanCord + 1
            tileMap[lastPacmanCord] = " "
            tileMap[pacmanCord] = "©"
    elif tPacman == turnPacman.up:
        lastPacmanCord = pacmanCord
        if tileMap[pacmanCord - lenMap] == ' s':
            score += 1
        if tileMap[pacmanCord - lenMap] != '#':
            pacmanCord = pacmanCord - lenMap
            tileMap[lastPacmanCord] = " "
            tileMap[pacmanCord] = "©"
    elif tPacman == turnPacman.down:
        lastPacmanCord = pacmanCord
        if tileMap[pacmanCord + lenMap] == ' s':
            score += 1
        if tileMap[pacmanCord + lenMap] != '#':
            pacmanCord = pacmanCord + lenMap
            tileMap[lastPacmanCord] = " "
            tileMap[pacmanCord] = "©"
    to = Pinki.algo()
    Pinki.goTo(to)
    tileN = False
    clear_screen()

    tileMap[teleport1Cord] = "t"
    tileMap[teleport2Cord] = "t"
    tileMap[Pinki.cord] = Pinki.name
    
    tileMap[teleport2Cord + 1] = "#"
    for i in range(len(tileMap)):
        global scoresCords
        global winScreen
        global gameWin
        
        if score == 1000:
            gameWin = True
            gameOver = True
        if (' s' in tileMap) == False:
            for i in range(len(scoresCords)):
                if pacmanCord != scoresCords[i]:
                   tileMap[scoresCords[i]] = ' s'
        if ('©' in tileMap) == False:
            gameOver = True

        if tileMap[i] == "#":
            if tileN == True:
                colorPrint('###', colorTerm.default)
                tileN = False
            else:
                colorPrint('###', colorTerm.default)
                if tileMap[i + 1] == "n":
                  tileN = True
        elif i == teleport2Cord:
            colorPrint('▀▀▀', colorTerm.blue)
        elif i == teleport1Cord:
            colorPrint('▀▀▀', colorTerm.blue)
        elif tileMap[i] == "k":
            colorPrint('#', colorTerm.default)
        elif tileMap[i] == " s":
            scoresExists = True
            colorPrint('▀▀▀', colorTerm.white)
        elif tileMap[i] == " ":
            colorPrint('▀▀▀', colorTerm.default)
            tileN = False
            if tileMap[i + 2] == "n":
                  tileN = True
        elif tileMap[i] == "n":
            colorPrint('\n', colorTerm.default)
            tileN = True
        elif tileMap[i] == "l":
            colorPrint('###', colorTerm.default)
        elif tileMap[i] == "©":
            colorPrint('©©©', colorTerm.yellow)
        elif tileMap[i] == "SCORE":
            colorPrint("\t\tSCORE = " + str(score) + "\t\t", colorTerm.default)
        elif tileMap[i] == "t":
            colorPrint('▀▀▀', colorTerm.blue)
        elif tileMap[i] == "teleport1Cord":
            colorPrint("\tteleport1Cord = " + str(teleport1Cord) + "\t", colorTerm.default)
        elif tileMap[i] == "teleport2Cord":
            colorPrint("\tteleport2Cord = " + str(teleport2Cord) + "\t", colorTerm.default)
        elif tileMap[i] == "pacmanCord":
            colorPrint("\tpacmanCord = " + str(pacmanCord) + "\t", colorTerm.default)
        elif tileMap[i] == "lastPacmanCord":
            colorPrint("\tlastPacmanCord = " + str(lastPacmanCord) + "\t",colorTerm.default)
        elif tileMap[i] == Pinki.name:
            colorPrint('▀'+ Pinki.name +'▀', Pinki.color)
        else:
            FatalError = True
def input_up():
    global tPacman
    tPacman = turnPacman.up
def input_left():
    global tPacman
    tPacman = turnPacman.left
def input_down():
    global tPacman
    tPacman = turnPacman.down
def input_right():
    global tPacman
    tPacman = turnPacman.right
def input():
    keyboard.add_hotkey('w', input_up)
    keyboard.add_hotkey('a', input_left)
    keyboard.add_hotkey('s', input_down)
    keyboard.add_hotkey('d', input_right)

    
def setup():
    global scoresCords
    global lenMap
    global teleport1Cord
    global teleport2Cord
    i = 0
    while True:
        if teleport1Cord == 0:
            if tileMap[i] == "t":
                teleport1Cord = i 
            i += 1
        elif teleport2Cord == 0:
            if tileMap[i] == "t":
                teleport2Cord = i 
                break
            i += 1
    i = 0
    while True:
        if tileMap[i] == "n":
            lenMap = i + 1
            break
        i += 1
    global pacmanCord 
    global lastPacmanCord 
    i = 0
    while True:
        if tileMap[i] == "©":
            pacmanCord = i 
            lastPacmanCord = pacmanCord
            break
        i += 1
    i = 0
    j = 0
    for i in range(len(tileMap)):
        for j in range(len(tileMap)):
            
            if tileMap[j] == " s":
                scoresCords.append(j)  
            if len(tileMap) - 1 == i:
                break
        break
    i = 1
def fatalOut():
    global errMsg
    print("FATAL: " + errMsg)
def showWinScreen():
    clear_screen()
    synbol = "###"
    for i in range(10):
        print(synbol * 21)
    print(synbol * 10 + colored('YOU', 'black', 'on_green') + synbol * 10)
    print(synbol * 10 + colored('WIN', 'black', 'on_green') + synbol * 10)
    for i in range(10):
        print(synbol * 21)
    
def showGameOverScreen():
    clear_screen()
    synbol = "###"
    for i in range(10):
        print(synbol * 21)
    print(synbol * 10 + colored('GAME', 'black', 'on_red') + synbol * 9 + "##")
    print(synbol * 10 + colored('OVER', 'black', 'on_red') + synbol * 9 + "##")
    for i in range(10):
        print(synbol * 21)
def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')

def main():
    global FatalError
    global gameSpeed
    setup()
    while gameOver == False:
        time.sleep(gameSpeed)
        if FatalError == False:
            draw()
            input()
        else:
            clear_screen()
            fatalOut()
    if gameWin:
        while True:
            time.sleep(gameSpeed)
            
            showWinScreen()
    else:
        showGameOverScreen()

if __name__=="__main__": 
    main() 


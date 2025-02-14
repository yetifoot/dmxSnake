import sys
import os
import pygame, time
import array
import numpy as np
import random
from ola.ClientWrapper import ClientWrapper
################################# DEFINE VARIABLES AND INITIALIZE #################################
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Calibri',20)
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 40
#define menu colors
WHITE = (255,255,255)
BLACK = (0,0,0)
#define dmx colors
dmxWHITE = np.array([255, 255, 255])
dmxBLACK = np.array([0, 0, 0])
dmxRED = np.array([255, 0, 0])
dmxBLUE = np.array([0, 0, 255])
dmxGREEN = np.array([0, 255, 0])
dmxTEAL = np.array([0, 100, 255])
dmxPINK = np.array([255, 0, 75])
#read highscore if available
highscorePath = 'highscore.txt'
if os.path.exists(highscorePath):
    with open(highscorePath, 'r') as file:
        txtstring = file.read()
        highscore = int(txtstring)
else:
    highscore = 0
#set up game variables
snakehead = np.array([4, 4])
direction = np.array([0, 0])
snakeHistory = np.array([], dtype=int)
historyFlip = np.flip(snakeHistory)
timer = 0
#controls speed of snake
velocity = 2
prev_time = time.time()
dt = 0
record = 0
passed, start = False, False
alive = True
moved = False
reset = False
score = 0
FPS = 40
pxlWidth = 8
pxlHeight = 16
intens = 0.5
#set dmx universe for OLA
universe = 2
cellsize = 20
length = 1
food = np.array([2, 2])
gamearray = np.zeros((pxlWidth, pxlHeight), dtype=int)
dmxarray = np.zeros((170, 3), dtype=np.uint8)
def DmxSent(state):
        wrapper.Stop()
################################# GAME LOOP ##########################
while running:
    # Limit framerate
    clock.tick(FPS)
    # Compute delta time
    now = time.time()
    dt = now - prev_time
    prev_time = now
    #check for reset after game over
    if reset == True:
        start = True
        alive = True
        moved = False
        length = 1
        food = np.array([2, 2])
        snakehead = np.array([4, 4])
        direction = np.array([0, 0])
        snakeHistory = np.array([], dtype=np.uint8)
        reset = False
    # main loop
    if start:
        timer += dt
        #move snake head
        foodXint = int(food[0])
        foodYint = int(food[1])
        oldheadint = np.rint(snakehead)
        oldheadXint = int(oldheadint[0])
        oldheadYint = int(oldheadint[1])
        headX = snakehead[0] + direction[0] *dt *velocity
        headY = snakehead[1] + direction[1] *dt *velocity
        snakehead = np.array((headX, headY))
        #check if out of bounds. includes a buffer zone from the precise math to give the player a little wiggle room with the big pixels
        if headX < -0.4 or headX > pxlWidth-0.6:
            alive = False
        if headY < -0.4 or headY > pxlHeight-0.6:
            alive = False
        ################################# UPDATE GAME ARRAY ##########################
        #reset game array
        gamearray.fill(0)
        tailArray = np.array([])
        headint = np.rint(snakehead)
        headXint = int(headint[0])
        headYint = int(headint[1])
        #calculate and update tail array
        if length > 1:
            historyFlip = np.flip(snakeHistory)
            for i in range(0, length):
                tailX = historyFlip[2*i+1]
                tailY = historyFlip[2*i]
                gamearray[tailX, tailY] = 2
        #check if snake moved
        if oldheadXint == headXint and oldheadYint == headYint:
            moved = False
        else:
            moved = True
        #move the snake
        if moved == True:
            #update snake history
            snakeHistory = np.append(snakeHistory, [headXint,headYint])
            #eatfood
            eatfood = np.array_equal(food, headint)
            if eatfood == True:
                length += 1
                food = np.array([random.randint(0, pxlWidth-1), random.randint(0, pxlHeight-1)])
                foodXint = int(food[0])
                foodYint = int(food[1])
            #check if we ate our tail before we draw the head
            if gamearray[headXint, headYint] == 2:
                alive = False
        #update food and head on the array
        gamearray[foodXint, foodYint] = 3
        gamearray[headXint, headYint] = 1
        
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        #check if we want to quit
        if event.type == pygame.QUIT:
            running = False
        #check movement input and stop the player from eating their own tail
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
            if event.key == pygame.K_LEFT:
                suicide = np.array_equal(direction, [0, 1])
                if suicide:
                    direction = [0, 1]
                else:
                    direction = [0, -1]
            if event.key == pygame.K_RIGHT:
                suicide = np.array_equal(direction, [0, -1])
                if suicide:
                    direction = [0, -1]
                else:
                    direction = [0, 1]
            if event.key == pygame.K_UP:
                suicide = np.array_equal(direction, [1,0])
                if suicide:
                    direction = [1, 0]
                else:
                    direction = [-1, 0]
            if event.key == pygame.K_DOWN:
                suicide = np.array_equal(direction, [-1,0])
                if suicide:
                    direction = [-1, 0]
                else:
                    direction = [1, 0]
            #check intensity input
            if event.key == pygame.K_1:
                intens = 0.1
            if event.key == pygame.K_2:
                intens = 0.2
            if event.key == pygame.K_3:
                intens = 0.3
            if event.key == pygame.K_4:
                intens = 0.4
            if event.key == pygame.K_5:
                intens = 0.5
            if event.key == pygame.K_6:
                intens = 0.6
            if event.key == pygame.K_7:
                intens = 0.7
            if event.key == pygame.K_8:
                intens = 0.8
            if event.key == pygame.K_9:
                intens = 0.9
            if event.key == pygame.K_0:
                intens = 1
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    ################################# SET UP MENU #################################
    fps_text = font.render("FPS: " +str(round(clock.get_fps(),2)), False, (255,255,255))
    intens_text = font.render("| Press Space to Start | Intensity: " +str(intens*100), False, (255,255,255))
    ###################################### UPDATE DMX ##########################################
    #get gamearray ready for dmx conversion
    convertarray = gamearray.flatten()
    #set the colors for head tail and food
    col1LVL = dmxTEAL*intens
    col1LVL = np.rint(col1LVL)
    col2LVL = dmxPINK*intens
    col2LVL = np.rint(col2LVL)
    col3LVL = dmxGREEN*intens
    col3LVL = np.rint(col3LVL)
    #put colors into dmxarray
    for i in range(0,pxlHeight*pxlWidth):
        if convertarray[i] == 0:
            dmxarray[i] = dmxBLACK
        if convertarray[i] == 1:
            dmxarray[i] = col1LVL
        if convertarray[i] == 2:
            dmxarray[i] = col1LVL
        if convertarray[i] == 3:
            dmxarray[i] = col2LVL
    #use ola to send dmx frame
    dmxpacket = dmxarray.tobytes()
    data = array.array('B', dmxpacket)
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()
    ################################# UPDATE WINDOW AND DISPLAY ################################
    canvas.fill((0, 0, 0))
    canvas.blit(fps_text, (0, 0))
    canvas.blit(intens_text, (150, 0))
    ################################# CHECK IF DEAD ################################
    #debug prints
    #print(gamearray)
    if alive == False:
        gameover = font.render("GAME OVER MASH SPACE TO RESTART", False, (255,255,255))
        canvas.blit(gameover, (50, DISPLAY_H/2))
        if length > highscore:
            highscore = length
            with open(highscorePath, 'w') as file:
                file.write(str(highscore))
        hsdisplay = font.render("High Score: " + str(highscore), False, (255,255,255))
        canvas.blit(hsdisplay, (DISPLAY_W/2-50, DISPLAY_H/2-50))
        start = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset = True
    ################################# RENDER WINDOW ################################
    window.blit(canvas, (0,0))
    pygame.display.update()








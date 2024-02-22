# the main folder, run the game from here

snakeNum = 1 # change this for more snakes

import pygame as pg
import tile as t
import random

pg.init()

rand = random.Random()

xTileNum = 10
yTileNum = 10

screen = pg.display.set_mode((xTileNum * 50, yTileNum * 50))

running = True
started = False # this makes sure the game doesnt start until the player moves
killed = False

tileArray = [[] for _ in range(xTileNum)] # accessing any tile is [x][y]

pg.time.set_timer(pg.USEREVENT + 1, 1) # every milisecond we can get this event

snakeFrames = 500 # this is how many frames it takes for the snake to move, and it can go down the longer the game lasts
snakeFrame = 0

applesEaten = 0

def startGame(): # does everything needed for the game to start
    global snakeFrame, snakeFrames, started, tileArray, applesEaten

    snakeFrames = 500 # this is how many frames it takes for the snake to move, and it can go down the longer the game lasts
    snakeFrame = 0

    applesEaten = 0

    started = False # this makes sure the game doesnt start until the player moves
    
    # gets rid of the previous apples and heads
    t.apples.clear()
    t.heads.clear()

    tileArray = [[] for _ in range(xTileNum)] # accessing any tile is [x][y]

    for xNum in range(xTileNum):
        for yNum in range(yTileNum):
            tileArray[xNum].append(t.Tile(xNum, yNum))

    t.Apple(4, 2, tileArray)

    for _ in range(snakeNum):
        randX = rand.randint(2, xTileNum - 4) # gives some room
        randY = rand.randint(2, yTileNum - 4)

        mainhead = t.SnakeHead(randX, randY, tileArray)
        # adds 2 body parts automatically
        mainhead.addBody(tileArray)
        mainhead.addBody(tileArray)

startGame() # does the first start of the game

while running == True:
    for xTiles in tileArray: # place all tiles onto the screen
        for tile in xTiles:
            if (tile.obj == None): # if there is nothing on the tile, we cont use the tiles obj as its color, so we make it black
                pg.draw.rect(screen, [0,0,0], [tile.x * 50, tile.y * 50, 50, 50]) # draws the main color of the tile
                pg.draw.rect(screen, [255,255,255], [tile.x * 50, tile.y * 50, 50, 50], 1) # draws the small outline

            else:
                pg.draw.rect(screen, tile.obj.color, [tile.x * 50, tile.y * 50, 50, 50]) # draws the main color of the tile
                pg.draw.rect(screen, [255,255,255], [tile.x * 50, tile.y * 50, 50, 50], 1) # draws the small outline

    killed = True
    for head in t.heads:
        if (head.direction != "dead"):
            killed = False # if even a single snake is alive, it counts it as still alive

    if (killed == True):
        startGame()

    for apple in t.apples:
        if (apple.eaten == True):
            apple.place(tileArray) # places the apple randomly if it was eaten

            applesEaten += 1

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            moved = False

            for head in t.heads:
                if (head.direction != "dead"): # keeps the head dead
                    if event.key == pg.K_w: # up
                        head.changeDirection(tileArray, "up")
                        moved = True

                    elif event.key == pg.K_s: # down
                        head.changeDirection(tileArray, "down")
                        moved = True

                    elif event.key == pg.K_a: # left
                        head.changeDirection(tileArray, "left")
                        moved = True

                    elif event.key == pg.K_d: # right
                        head.changeDirection(tileArray, "right")
                        moved = True

            # to make sure the game starts
            if (moved == True and started == False):
                started = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                running = False

            if event.key == pg.K_r:
                startGame() # resets the game if the r button is pressed

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.USEREVENT + 1:
            if killed == False and started == True:
                snakeFrame += 1

                if (snakeFrame >= snakeFrames - (applesEaten * 3)):
                    snakeFrame = 0

                    for head in t.heads:
                        head.move(tileArray)

    pg.display.flip() # displays all changes tot he screen

pg.quit() # ends the program nicely
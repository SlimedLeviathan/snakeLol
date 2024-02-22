# the main folder, run the game from here

import pygame as pg
from tile import Tile

pg.init()

xTiles = 10
yTiles = 10

screen = pg.display.set_mode((xTiles * 50, yTiles * 50))

running = True
started = False # this makes sure the game doesnt start until the player moves

tileArray = [[] for _ in range(xTiles)] # accessing any tile is [x][y]

for xNum in range(xTiles):
    for yNum in range(yTiles):
        tileArray[xNum].append(Tile(xNum, yNum))

while running == True:

    for xTiles in tileArray:
        for tile in xTiles:
            if (tile.obj == None): # if there is nothing on the tile, we cont use the tiles obj as its color, so we make it black
                pg.draw.rect(screen, [0,0,0], [tile.x * 50, tile.y * 50, 50, 50]) # draws the main color of the tile
                pg.draw.rect(screen, [255,255,255], [tile.x * 50, tile.y * 50, 50, 50], 1) # draws the small outline

            else:
                pg.draw.rect(screen, tile.obj.color, [tile.x * 50, tile.y * 50, 50, 50]) # draws the main color of the tile
                pg.draw.rect(screen, [255,255,255], [tile.x * 50, tile.y * 50, 50, 50], 1) # draws the small outline

    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                running = False

        if event.type == pg.QUIT:
            running = False

    pg.display.flip() # displays all changes tot he screen

pg.quit() # ends the program nicely
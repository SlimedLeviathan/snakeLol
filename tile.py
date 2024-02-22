# this file contains the tile class and all objects, which is how everything works
import random

rand = random.Random()

def getDirection(direction): # really easy function
    if direction == "up":
        return [0,-1]
    elif direction == "down":
        return [0,1]
    elif direction == "left":
        return [-1,0]
    elif direction == "right":
        return [1,0]

    return [0,0] # for anything else

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.obj = None # whats ontop of the tile

class TileObject:
    def __init__(self, x, y, color, tileArray):
        self.x = x
        self.y = y
        
        self.color = color

        tileArray[x][y].obj = self # sets the tiles obj to this obj

class SnakeBody(TileObject): # this is the other tiles of the player
    def __init__(self, x, y, tileArray, direction, child = None):
        TileObject.__init__(self, x, y, [0,255,0], tileArray)

        self.direction = direction # the direction the snakes body will go next

        self.child = child

    def addBody(self, tileArray): # makes a new body
        if (self.child == None): # if the head doesnt have one it adds it to behind where its going
            forces = getDirection(self.direction)

            self.child = SnakeBody(self.x + -forces[0], self.y + -forces[1], tileArray, self.direction) # makes a new snake body

        else: # otherwise it tells the next bodies to do the same
            if (self.child.direction == "dead"):
                self.child = None # basically tell the program to redo this without looking at the child
                self.addBody(tileArray)

            else:
                self.child.addBody(tileArray)

    def move(self, tileArray):
        force = getDirection(self.direction)

        force[0] += self.x
        force[1] += self.y

        if not (force[0] > len(tileArray) - 1 or force[1] > len(tileArray[0]) - 1 or force[0] < 0 or force[1] < 0): # making sure the snake doesnt go outside the bounds of the game
            tile = tileArray[force[0]][force[1]]

            if (tile.obj != None): # if there is something on the tile, we do the hit function
                tile.obj.hit(self, tileArray)

            else:
                # the tile this body was just on should have nothing on it 
                tileArray[self.x][self.y].obj = None

                tile.obj = self # and otherwise this snake body inhabits it
                
                self.x = force[0]
                self.y = force[1]

                if (self.child != None):
                    self.child.move(tileArray)

                    if (self.child.direction != "dead"): # keeps them dead
                        self.child.direction = self.direction # after the child moves in the direction it is supposed to, we set its direction to this ones now, which allows the snake to turn

                    else:
                        self.child = None

        else:
            self.kill()

    def hit(self, snake, tileArray):
        snake.kill()

    def kill(self):
        if (self.child != None):
            self.child.kill()

        self.color = [150, 150, 150] # gray to represent death

        self.direction = "dead" # should stop the snake from moving

heads = []
# this is where the player controls the snake from
class SnakeHead(SnakeBody): # only one of these SHOULD be made, but ill make a mode for multiple
    def __init__(self, x, y, tileArray, direction = "up"):
        SnakeBody.__init__(self, x, y, tileArray, direction)

        heads.append(self)

    def changeDirection(self, tileArray, direction):
        force = getDirection(direction)

        tile = tileArray[self.x + force[0]][self.y + force[1]]

        if (tile.obj != self.child or tile.obj == None):
            self.direction = direction

apples = []
class Apple(TileObject):
    def __init__(self, x, y, tileArray):
        TileObject.__init__(self, x, y, [255,0,0], tileArray)

        self.eaten = False # so that the apple can gets set after the snake is made

        apples.append(self)

    def hit(self, snake, tileArray):
        self.eaten = True # set up for the apple to move to a different spot
        tileArray[self.x][self.y].obj = None # make sure the apple get destroyed

        snake.addBody(tileArray)
        snake.move(tileArray) # this allows the snake to continue moving

    def place(self, tileArray):
        xRange = len(tileArray)
        yRange = len(tileArray[0])
        
        while (self.eaten == True):
            randX = rand.randint(0, xRange - 1) # gets random placement
            randY = rand.randint(0, yRange - 1)

            if (tileArray[randX][randY].obj == None): # checks that its empty
                tileArray[randX][randY].obj = self # places itself

                self.x = randX
                self.y = randY

                self.eaten = False # and stops the loop
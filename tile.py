# this file contains the tile class and all objects, which is how everything works
def getDirection(direction): # really easy function
    if direction == "up":
        return [0,-1]
    elif direction == "down":
        return [0,1]
    elif direction == "left":
        return [-1,0]
    elif direction == "right":
        return [1,0]

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.obj = None # whats ontop of the tile

class TileObject:
    def __init__(self, x, y, name, color, tileArray):
        self.x = x
        self.y = y
        
        self.color = color

        self.name = name

        tileArray[x][y].obj = self # sets the tiles obj to this obj

# this is where the player controls the snake from
class SnakeHead(TileObject): # only one of these SHOULD be made, but ill make a mode for multiple
    def __init__(self, x, y, child, tileArray):
        TileObject.__init__(self, x, y, "head", [50,255,50], tileArray)

        self.direction = "up" # the direction of the snakes movement, dictated by the player

        self.child = child # the next body part in line

    def addBody(self, tileArray): # makes a new body
        if (self.child == None): # if the head doesnt have one it adds it to behind where its going
            forces = getDirection(self.direction)

            self.child = SnakeBody(self.x + -forces[0], self.y + -forces[1], self.direction, tileArray) # makes a new snake body

        else: # otherwise it tells the next bodies to do the same
            self.child.addBody()

class SnakeBody(TileObject): # this is the other tiles of the player
    def __init__(self, x, y, tileArray, direction, child = None):
        TileObject.__init__(self, x, y, "body", [0,255,0], tileArray)

        self.direction = direction # the direction the snakes body will go next

        self.child = child

    def addBody(self, tileArray): # same as snake head add body
        if (self.child == None): # if no child, add behind it
            forces = getDirection(self.direction)

            self.child = SnakeBody(self.x + -forces[0], self.y + -forces[1], self.direction, tileArray) # makes a new snake body

        else: # otherwise it tells the next body to do it
            self.child.addBody()
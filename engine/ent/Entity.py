class Entity:
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xSpeed = 250
        self.ySpeed = 250
        self.maxSpeed = 250
        self.horDir = 0
        self.verDir = 0
        self.dead = False
        self.color = "black"
        
    def update(self, canvas, delta):
        self.draw(canvas)
        self.move(delta)
        
        if self.x > 640:
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = 640
        
        if self.y > 480:
            self.y = -self.height
        elif self.y + self.height < 0:
            self.y = 480
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y,
                                self.x + self.width, self.y + self.height,
                                fill=self.color)
        
    def move(self, delta):
        self.x += (delta * self.xSpeed) 
        self.y += (delta * self.ySpeed)

    def moveHor(self, dir):
        #left = -1, right = 1
        self.xSpeed = self.maxSpeed * dir
        self.horDir = dir
    
    def stopHor(self):
        self.xSpeed = 0
        self.horDir = 0
    
    def moveVer(self, dir):
        #down = 1, up = -1
        self.ySpeed = self.maxSpeed * dir
        self.verDir = dir
        
    def stopVer(self):
        self.ySpeed = 0
        self.verDir = 0
        
    #Abstract
    def collidedWith(self, other):
        raise NotImplementedError

    def destroy(self):
        self.dead = True
        self.game.removeEnt(self)

    def isDead(self):
        return self.dead
        
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def getWidth(self):
        return self.width
        
    def getHeight(self):
        return self.height
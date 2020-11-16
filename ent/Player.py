import tkinter

from engine.ent.Entity import *
from ent.Enemy import *

class Player(Entity):
    def __init__(self, game, difficulty):
        super().__init__(game, 100, 100, 30, 30)
        self.health = 3 - difficulty
        self.maxSpeed = 500 + (difficulty * 50)
        self.xSpeed = self.maxSpeed
        self.ySpeed = 0
        self.invincible = False
        self.invincibleTimer = 0
        self.invincibleTimerMax = 90
        self.color = "white"

        self.images = {
            "down": tkinter.PhotoImage(file="res/shipDown.gif", master=game.canvas),
            "left": tkinter.PhotoImage(file="res/shipLeft.gif", master=game.canvas),
            "up": tkinter.PhotoImage(file="res/shipUp.gif", master=game.canvas),
            "right": tkinter.PhotoImage(file="res/shipRight.gif", master=game.canvas),
        }
        self.image = self.images["right"]
        
    def update(self, canvas, delta):
        super().update(canvas, delta)

        if self.invincible:
            self.invincibleTimer += 1
            if self.invincibleTimer > self.invincibleTimerMax:
                self.invincible = False
                self.invincibleTimer = 0            

    def draw(self, canvas):
        if self.invincible and self.invincibleTimer % 2 == 0:
            return
        # super().draw(canvas)
        canvas.create_image(self.x, self.y, image=self.image,
                            state="normal")
        
    def collidedWith(self, other):
        if type(other) == Enemy and self.invincible is False:
            self.health -= 1
            self.invincible = True
            if self.health <= 0:
                self.dead = True
        
    def getHealth(self):
        return self.health
    
    def setImage(self, img):
        self.image = self.images[img]
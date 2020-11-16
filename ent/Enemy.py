from engine.ent.Entity import *

class Enemy(Entity):
    def __init__(self, game, x, y, xSpeed, ySpeed):
        super().__init__(game, x, y, 20, 20)
        self.color = "red"
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed

    def collidedWith(self, other):
        if self.dead is True:
            return
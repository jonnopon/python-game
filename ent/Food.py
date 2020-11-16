from engine.ent.Entity import *
from ent.Player import *

class Food(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 15, 15)
        self.color = "green"
    
    def update(self, canvas, delta):
        self.draw(canvas)
    
    def move(self, delta):
        return
        
    def collidedWith(self, other):
        if self.dead is True:
            return
            
        if type(other) == Player:
            self.game.addPoint()
            self.destroy()
        
    def destroy(self):
        super().destroy()
        self.game.genFood()
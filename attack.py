import types
from random import randint, uniform
import os

from engine.ent.Entity import *
from engine.util.State import *
from engine.Game import *
from ent.Enemy import *
from ent.Food import *
from ent.Player import *

"""Construct the Abstract Game object, setting its width and height"""
game = Game(640, 480)

"""STEP 1: define game initial attributes in dictionary"""
gameData = {
    "ents": [],
    "points": 0,
    "enemyGend": False,
    "highScores": [0, 0, 0],
    "highScoreFileName": "highscore.txt",
    "highScoreAchieved": False,
    "menuSelection": 0,
    "difficulty": 0,
    "canChangeMenu": True,
    "menuTimer": 0,
    "menuTimerMax": 5,
    "menuTimeout": True,
    "menuTimeoutTimer": 0,
    "menuTimeoutTimerMax": 20
}

"""STEP 2: define which attributes should reinitialise on game reset"""
gameReinitData = {
    "ents": [],
    "points": 0,
    "menuTimeout": True,
    "highScoreAchieved": False,
    "enemyGend": False,
    "menuSelection": 0,
}

"""STEP 4: define game init function"""
"""self refers to game since this method will be injected"""
def initFunc(self):
    self.loadAttributes(self.initData)
    self.activeState("menu")
    
    self.player = Player(self, 0)
    self.ents.append(self.player)
    self.genFood()

    for file in os.listdir():
        if file == self.highScoreFileName:
            highScoreFile = open(file, "r")
            self.highScores = highScoreFile.readlines()
            x = []
            for highScore in self.highScores:
                if highScore.find("\n") > 0:
                    x.append(highScore)     
            self.highScores = x
            highScoreFile.close()
            break
    
    self.gameLoop()

"""STEP 5: define game reinit function"""
"""self refers to game since this method will be injected"""
def reinitFunc(self):
    self.loadAttributes(self.reinitData)
    self.activeState("menu")
    
    self.player = Player(self, 0)
    self.ents.append(self.player)
    self.genFood()

"""STEP 6: attach init and reinit data to the Game object"""
game.addAttr("initData", gameData)
game.addAttr("reinitData", gameReinitData)

"""STEP 7: attach init func and reinit func to Game object"""
game.addMethod(initFunc)
game.addMethod(reinitFunc)

"""STEP 8: define global utility methods for Game"""
"""self refers to game since this method will be injected"""
#define and add game methods
def genFood(self):
    self.addEnt(Food(self, randint(0, 600), randint(0, 440)))

def genEnemy(self):
    if self.enemyGend is False:
        moveHor = randint(0, 100) < 50
        moveVer = moveHor is False
        xSpeed = 0
        ySpeed = 0
        
        if moveHor == True:
            xSpeed = uniform(-400, 400)
        elif moveVer == True:
            ySpeed = uniform(-400, 400)
            
        self.addEnt(Enemy(self, randint(0, 640), randint(0, 480),
                            xSpeed, ySpeed))

def addPoint(self):
        self.points += 1

"""STEP 9: attach utility methods to Game object by name"""
game.addMethod(genFood)
game.addMethod(genEnemy)
game.addMethod(addPoint)

"""STEP 10: define Game State function bodies describing the frame of each state"""
"""a state function can take any number of params as long as denoted in assignment to Game"""
"""for this simple game, just passing the Game object"""
def menuFunc(game):
    game.canvas.create_text(320, 50, text="WELCOME", fill="white",
                                font=("monospace", 30))
                                
    game.canvas.create_text(320, 125, text="Difficulty", fill="white",
                            font=("monospace", 30))
    game.canvas.create_text(320, 150, text="(W / S to select)", fill="white",
                            font=("monospace", 15))
                            
    game.canvas.create_text(320, 200, text="Easy", fill="white",
                            font=("monospace", 20))
    game.canvas.create_text(320, 250, text="Medium", fill="white",
                            font=("monospace", 20))
    game.canvas.create_text(320, 300, text="Hard", fill="white",
                            font=("monospace", 20))
                            
    game.canvas.create_text(320, 400, text="space to start", fill="white",
                            font=("monospace", 25))
    game.canvas.create_text(320, 450, text="High Score: " +
                            str(game.highScores[game.menuSelection]),
                            fill="white", font=("monospace", 25))
        
    if game.canChangeMenu:
        if game.keyCodes.w in game.keys \
            or game.keyCodes.upArrow in game.keys \
            or game.keyCodes.numPad8 in game.keys:
                
            game.menuSelection -= 1            
            if game.menuSelection < 0:
                game.menuSelection = 2
            game.canChangeMenu = False
            
        elif game.keyCodes.s in game.keys \
            or game.keyCodes.downArrow in game.keys \
            or game.keyCodes.numPad5 in game.keys:
                
            game.menuSelection += 1            
            if game.menuSelection > 2:
                game.menuSelection = 0
            game.canChangeMenu = False
    else:
        game.menuTimer += 1
        if game.menuTimer > game.menuTimerMax:
            game.menuTimer = 0
            game.canChangeMenu = True
        
    if game.menuSelection == 0:
        game.canvas.create_text(250, 200, text=">", fill="white",
                            font=("monospace", 15))
    elif game.menuSelection == 1:
        game.canvas.create_text(250, 250, text=">", fill="white",
                            font=("monospace", 15))
    elif game.menuSelection == 2:
        game.canvas.create_text(250, 300, text=">", fill="white",
                            font=("monospace", 15))
        
    if (game.keyCodes.space in game.keys \
        or game.keyCodes.enter in game.keys) \
        and game.menuTimeout is False:
            
        game.activeState("game")
        game.difficulty = game.menuSelection
        
        game.ents = []
        game.player = Player(game, game.difficulty)
        game.ents.append(game.player)
        game.genFood()
        game.menuTimeout = True
        
    if game.menuTimeout is True:
        game.menuTimeoutTimer += 1
        if game.menuTimeoutTimer > game.menuTimeoutTimerMax:
            game.menuTimeoutTimer = 0
            game.menuTimeout = False
            
def gameFunc(game):
    if len(game.ents) <= 1:
        x =10
        
    for i in range(len(game.ents)):
        game.ents[i].update(game.canvas, game.delta)
        
        for j in range(i + 1, len(game.ents)):
            if j >= len(game.ents):
                x = 10
                
            if game.checkEntCollision(game.ents[i], game.ents[j]) is True:
                game.ents[i].collidedWith(game.ents[j])
                game.ents[j].collidedWith(game.ents[i])
        
    if game.keyCodes.a in game.keys \
        or game.keyCodes.leftArrow in game.keys \
        or game.keyCodes.numPad4 in game.keys:
            
        game.player.moveHor(-1)
        game.player.stopVer()
        
    elif game.keyCodes.d in game.keys \
        or game.keyCodes.rightArrow in game.keys \
        or game.keyCodes.numPad6 in game.keys:
            
        game.player.moveHor(1)
        game.player.stopVer()
        
    elif game.keyCodes.w in game.keys \
        or game.keyCodes.upArrow in game.keys \
        or game.keyCodes.numPad8 in game.keys:
            
        game.player.moveVer(-1)
        game.player.stopHor()
        
    elif game.keyCodes.s in game.keys \
        or game.keyCodes.downArrow in game.keys \
        or game.keyCodes.numPad5 in game.keys:
        game.player.moveVer(1)
        game.player.stopHor()
        
    if game.keyCodes.p in game.keys \
        or game.keyCodes.esc in game.keys:
            
        game.activeState("paused")
        
    if game.points > 0 and game.points % 5 == 0:
        game.genEnemy()
        game.enemyGend = True
    else:
        game.enemyGend = False
        
    if game.player.isDead():
        game.activeState("dead")
        
    game.canvas.create_text(570, 20, text="Points: " + str(game.points),
                            fill="white", font=("monospace", 15))
    game.canvas.create_text(550, 60, text="High Score: " + 
                            str(game.highScores[game.difficulty]),
                            fill="white", font=("monospace", 15))
    game.canvas.create_text(60, 20, text="Health: " + str(game.player.getHealth()),
                            fill="white", font=("monospace", 15))

def pausedFunc(game):
    for i in range(len(game.ents)):
        game.ents[i].update(game.canvas, 0)
            
    if game.keyCodes.space in game.keys:
        game.activeState("game")
        
    game.canvas.create_text(320, 240, text="PAUSED", fill="white",
                            font=("monospace", 20))
    game.canvas.create_text(320, 280, text="space to continue", fill="white",
                            font=("monospace", 20))
    game.canvas.create_text(570, 20, text="Points: " + str(game.points),
                            fill="white", font=("monospace", 15))
    game.canvas.create_text(550, 60, text="High Score: " + 
                            str(game.highScores[game.difficulty]),
                            fill="white", font=("monospace", 15))
    game.canvas.create_text(60, 20, text="Health: " + str(game.player.getHealth()),
                            fill="white", font=("monospace", 15))


def deadFunc(game):
    game.canvas.create_text(320, 50, text="DEAD", fill="white",
                                font=("monospace", 30))
    game.canvas.create_text(320, 150, text="space to restart", fill="white",
                            font=("monospace", 25))
    game.canvas.create_text(320, 400, text="Points: " + str(game.points),
                            fill="white", font=("monospace", 25))
                            
    if game.points > int(game.highScores[game.difficulty]):
        highScoreFile = open(game.highScoreFileName, "w")
        game.highScores[game.difficulty] = game.points
        for highScore in game.highScores:
            print(highScore, file=highScoreFile)
        highScoreFile.close()
        game.highScoreAchieved = True
    
    if game.highScoreAchieved:
        game.canvas.create_text(320, 450, text="New High Score!", fill="white",
                                font=("monospace", 25))
    else:
        game.canvas.create_text(320, 450, text="High Score: " +
                                str(game.highScores[game.difficulty]),
                                fill="white", font=("monospace", 25))
                                
    if game.keyCodes.space in game.keys:
        game.reinit()

"""STEP 11: construct States with names and function bodies"""
menuState = State("menu")
menuState.setFunc(menuFunc, game)
gameState = State("game")
gameState.setFunc(gameFunc, game)
pausedState = State("paused")
pausedState.setFunc(pausedFunc, game)
deadState = State("dead")
deadState.setFunc(deadFunc, game)

"""STEP 12: attach States to Game object"""
game.addState(menuState)
game.addState(gameState)
game.addState(pausedState)
game.addState(deadState)

"""STEP 13: choose an initially active state"""
game.activeState("menu")

"""STEP 14: start the game"""
game.start()
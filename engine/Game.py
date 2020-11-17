from tkinter import *
import time
import types
from engine.util.KeyCodes import *

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tk = Tk()
        self.frame=Frame(bg="black")
        self.frame.pack();
        
        #all references to rendering (window, canvas, shapes) will be absracted into renderer
        self.canvas = Canvas(self.tk, width=width, height=height)
        self.canvas.pack()
        self.tk.bind('<KeyPress>', self.onKeyPress)
        self.tk.bind('<KeyRelease>', self.onKeyRelease)

        self.states = {}
        self.currentState = None

        self.keys = set()
        self.keyCodes = KeyCodes()
        
        self.delta = 0
        self.lastLoopTime = 0

        self.initData = {}
        self.reinitData = {}
        self.initFunc = None
        self.reinitFunc = None
        
    def start(self):
        self.tk.after(1, self.init)
        self.tk.mainloop()
    
    def onKeyPress(self, event):
        # print(event.keycode)
        self.keys.add(event.keycode)

    def onKeyRelease(self, event):
        self.keys.remove(event.keycode)

    def keyPressed(self, keycode):
        return keycode in self.keys

    def addState(self, state):
        self.states[state.getName()] = state

    def activeState(self, name):
        self.currentState = self.states[name]

    def addEnt(self, e):
        self.ents.append(e)

    def removeEnt(self, e):
        self.ents.remove(e)

    def loadAttributes(self, data):
        for key in data:
            setattr(self, key, data[key])
            
    def addAttr(self, name, value):
        setattr(self, name, value)

    def addMethod(self, method):
        setattr(self, method.__name__, types.MethodType(method, self))

    def init(self):
        self.initFunc()

    def reinit(self):
        self.reinitFunc()        

    def gameLoop(self):
        while True:
            self.delta = time.time() - self.lastLoopTime;
            self.lastLoopTime = time.time()
            
            self.canvas.delete(ALL)
            self.canvas.create_rectangle(0, 0, 640, 480, fill="black")
                
            self.currentState.tick()
            
            self.tk.update_idletasks()
            self.tk.update()
    
    #will be moved to entity manager
    def checkEntCollision(self, e1, e2):
        x1 = e1.getX()
        x2 = e2.getX()
        y1 = e1.getY()
        y2 = e2.getY()
        w1 = e1.getWidth()
        w2 = e2.getWidth()
        h1 = e1.getHeight()
        h2 = e2.getHeight()
        
        #Do the rectangles collide?
        return x1 < (x2 + w2) and \
                (x1 + w1) > x2 and \
                y1 < (y2 + h2) and \
                (y1 + h1) > y2
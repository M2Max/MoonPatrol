from Background import Background
from Actor import Actor
from Rover import Rover
from Utility import Stats


class Arena():

    def __init__(self, size: (int, int), images: (str, str), score):
        self._w, self._h          = size
        self._imgCar, self._imgBG = images
        self._actors              = []
        self._backgrounds         = []
        self._stats               = Stats(score)

    def addActor(self, a: Actor):               #Adds Actor object to actors list
        if a not in self._actors:
            self._actors.append(a)

    def removeActor(self, a: Actor):            #Removes Actor object from actors list
        if a in self._actors:
            self._actors.remove(a)

    def addBackground(self, a: Background):     #Adds Background object to backgrounds list
        if a not in self._backgrounds:
            self._backgrounds.append(a)
    
    def removeBackground(self, a: Background):  #Removes Background object from backgrounds list
        if a in self._backgrounds:
            self._backgrounds.remove(a)

    #Move all item in arena
    def moveAll(self, points):        
        if self.canContinue():               
            self.moveSingleList(self._backgrounds)
            self.moveSingleList(self._actors)
            self._stats.addScore(points)
        else:
            for i in self.getRovers(): i.move()

    #Moves only the objects from the given list
    def moveSingleList(self, objects: list):   
        for obj in objects:
            obj.move()
            if(isinstance(obj, Actor)):
                self.check_collision(obj)

    #Check if a collision has occurred
    def check_collision(self, a):
        for other in self._actors:
            if other is not a and self.check(a, other):
                    a.collide(other)
                    other.collide(a)

    #Comparison of two items
    def check(self, a1: Actor, a2: Actor) -> bool:
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2 and 
                x2 < x1 + w1 and x1 < x2 + w2)

    #Function that checks if there is still at least one rover alive or in dead animation
    def canContinue(self):
        count = 0
        for i in self.getRovers(): 
            if i.isDead(): count += 1

        return not count == len(self.getRovers())

    #Function that stops the if there are no more rovers
    def canStop(self):
        return not len(self.getRovers()) == 0


    #Return the size of arena
    def size(self) -> (int, int):       return (self._w, self._h)

    #Return the image associated of Car
    def getImgCar(self) -> str:         return self._imgCar
    
    #Return the image associated of Background
    def getImgBG(self) -> str:          return self._imgBG
    
    #Return all background in arena
    def getBackgrounds(self) -> list:   return self._backgrounds

    #Return all actors in arena
    def getActors(self) -> list:        return self._actors

    #Return the main character
    def getRovers(self) -> list:        return [x for x in self._actors if isinstance(x, Rover)]

    #Return the stats
    def getStats(self) -> Stats:        return self._stats
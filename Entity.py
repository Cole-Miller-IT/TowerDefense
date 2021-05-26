import pygame
import random
import math
from pygame.locals import *
from pygame.math import Vector2

#--------------------------------------------------------------------------------------------
class Entity():
    def __init__(self, position):
        self.pos = position
        self.alive = True

    def processInput(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class Unit(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.pos = position
        self.move =Vector2(1, 0)
        self.size = Vector2(32, 32)
        self.angle = 0                  #Angle in degrees
        
        #Contains the location of the sprite texture in the spritesheet
        self.textureOrigin = Vector2(0, 0)

    #Computes the angle (in degrees) based on where the point is on the 2D plane
    def computeAngleDeg(self, targetedPoint):
        #Computes the angle in radians based on the unit's position and where it's looking
        theta = math.atan2(targetedPoint.y - self.pos.y, targetedPoint.x - self.pos.x)
        newAngle = math.degrees(theta) #Convert to degrees
        
        self.angle = newAngle
        
    def processInput(self):
        pass

    def update(self):
        if self.angle < 361:
            self.angle += 1

#A class that stores all variables and methods related to the player--------------------------------------------------------------------------------------------
class Player(Entity):
    def __init__(self, cellSize, worldSize):
        super().__init__(cellSize)  # Inherits all methods and attributes of the parent class
        pass

    def processInput(self):
        #self.clickPos = Vector2(pygame.mouse.get_pos())
        pass

    def update(self, points):
        pass
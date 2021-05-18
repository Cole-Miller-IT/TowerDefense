import pygame
import random
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
        self.movespeed = 0
        self.size = Vector2(32, 32)
        
        #Contains the location of the sprite texture in the spritesheet
        self.textureOrigin = Vector2(0, 0)

    def processInput(self):
        pass

    def update(self):
        pass

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
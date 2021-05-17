import pygame
import random
from pygame.draw import rect
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
    def __init__(self, gamestate, position):
        super().__init__(position)
        self.gamestate = gamestate
        self.pos = position
        self.movespeed = 0
        
        #
        self.tile = Vector2(0, 0)

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
        self.clickPos = Vector2(pygame.mouse.get_pos())

    def update(self, points):
        pass
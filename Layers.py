#Import Modules
import pygame
from pygame.locals import *
from pygame.math import Vector2
from GameState import GameState

class Layer():
    def __init__(self):
        self.gamestate = GameState()
        self.layers = self.gamestate.layers

    def render(self):
        pass

class EntityLayer(Layer):
    def render(self):
        pass
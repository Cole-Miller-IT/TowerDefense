#Import Modules
import pygame
from pygame.locals import *
from pygame.math import Vector2
from GameState import GameState

class Layer():
	def __init__(self, textureFile):
	    self.texture = pygame.image.load(textureFile)
	    #This loads the image faster when drawing
	    self.texture.convert() 
	
	#Renders a single tile
	def renderTile(self, pos, tile, gamestate):
	    cellSize = gamestate.cellSize
	    window = gamestate.window
	    
	    #Position, scaled to the games cell size
	    tilePos = pos.elementwise() * cellSize
	    
	    #Texture
	    textureOrigin = tile.elementwise() * cellSize
	    textureSurface = Rect(int(textureOrigin.x), int(textureOrigin.y), cellSize.x, cellSize.y)
	    
	    #Draw tile to the pygame surface
	    window.blit(self.texture, tilePos, textureSurface)
    
class ArrayLayer(Layer):
    def __init__(self, textureFile, array, gamestate):
        super().__init__(textureFile)
        self.array = array
        self.gamestate = gamestate
    
    #Renders all tiles contained in the array
    def render(self):
        for y in range(int(self.gamestate.worldSize.y)):
            for x in range(int(self.gamestate.worldSize.x)):
                tile = self.array[y][x]
                tilePosition = Vector2(x, y)
                if tile is not None:
                    self.renderTile(tilePosition, tile, self.gamestate)
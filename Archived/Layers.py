# Import Modules
import pygame
from pygame.locals import *
from pygame.math import Vector2

# A class that loads a spritesheet or texture file, then renders tiles, units, etc.. and draws them to the main game window


class Layer():
    def __init__(self, textureFile):
        self.texture = pygame.image.load(textureFile)
        # This loads the image faster when drawing
        self.texture.convert()

    def rotateTile(self, position, angle, texture, textureRect, surfaceSize):
        # Create a pygame surface, then blit the tile/units texture onto the surface at origin (0,0)
        tile = pygame.Surface((int(surfaceSize.x), int(surfaceSize.y)), pygame.SRCALPHA)
        tile.blit(texture, (0, 0), textureRect)

        # Rotate the tile
        rotatedTile = pygame.transform.rotate(tile, angle)

        new_rect = rotatedTile.get_rect(center=position)

        return (rotatedTile, new_rect)

    # Renders a single tile
    def renderTile(self, pos, tile, gamestate):
        cellSize = gamestate.cellSize
        window = gamestate.window

        # Position, scaled to the games cell size
        tilePos = pos.elementwise() * cellSize

        # Texture
        textureOrigin = tile.elementwise() * cellSize
        textureSurface = Rect(int(textureOrigin.x), int(textureOrigin.y), cellSize.x, cellSize.y)

        # Draw tile to the pygame surface
        window.blit(self.texture, tilePos, textureSurface)

    # Renders a single unit using its size, texture, and position
    def renderUnit(self, unit, window):
        # Create a Rect with the unit's size
        textureRect = Rect(int(unit.textureOrigin.x), int(unit.textureOrigin.y), unit.size.x, unit.size.y)

        # Rotates the turret to the targeted position  ***Currently just rotates the whole unit***
        if unit.angle != 0:
            # Rotate turret
            rotatedTile, rotatedPosition = self.rotateTile(unit.pos, unit.angle, self.texture, textureRect, unit.size)
            
            # Render Turret
            window.blit(rotatedTile, rotatedPosition)
            
        else:
            # Draw tile to the pygame surface
            window.blit(self.texture, unit.pos, textureRect)

# Used to create 2D arrays and display them to the window
class ArrayLayer(Layer):
    def __init__(self, textureFile, array, gamestate):
        super().__init__(textureFile)
        self.array = array
        self.gamestate = gamestate

    # Renders all tiles contained in the array (creates a 2D array of tiles and displays them to the window)
    def render(self):
        for y in range(int(self.gamestate.worldSize.y)):
            for x in range(int(self.gamestate.worldSize.x)):
                tile = self.array[y][x]
                tilePosition = Vector2(x, y)
                if tile is not None:
                    self.renderTile(tilePosition, tile, self.gamestate)

# Used to create a layer that contains all the current units
class UnitLayer(Layer):
    def __init__(self, textureFile, array, window):
        super().__init__(textureFile)
        self.array = array
        self.window = window

    # Renders all units
    def render(self):
        for unit in self.array:
            self.renderUnit(unit, self.window)


class HUDLayer(Layer):
    def __init__(self, textureFile, gamestate):
        super().__init__(textureFile)
        pygame.font.init()
        self.window = gamestate.window
        self.FPS = gamestate.FPS
        self.gamestate = gamestate

        # Font
        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        self.color = gamestate.blue
        self.FPSPos = Vector2(20, 20)

    def render(self):
        # Convert clock from a float to a int to round off decimal points
        FPS = int(self.gamestate.clock.get_fps())

        # Draw font/text
        fontSurface = self.font.render("FPS: " + str(FPS), True, self.gamestate.red)
        self.window.blit(fontSurface, (self.FPSPos.x, self.FPSPos.y))

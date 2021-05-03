#Import Modules
import pygame
from pygame.locals import *
from pygame.math import Vector2

#Contains the current game state
class GameState():
    def __init__(self):
        self.debug = True
        
        #Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.gray = (200, 200, 200)

        #FPS
        self.clock = pygame.time.Clock()
        self.FPS = 30

        #Game loop condition
        self.running = True

        #Window
        self.worldSize = Vector2(10, 10)
        self.cellSize = Vector2(64, 64)
        self.windowSize = self.worldSize.elementwise() * self.cellSize  # ie. A board of 10 x 10 tiles multiplied by the cellSize
        self.window = pygame.display.set_mode((int(self.windowSize.x), int(self.windowSize.y)))
        self.windowCaption = 'Tower Defense'

        #Enemies
        self.enemies = []

        #List of all keybinds
        self.hotkeys = [
            {	
                'menuItemName': 'Move Up',
                'hotkey': 'W', 
                'action': lambda: print('up') #commandMoveUp(Command)
            },
            {
                'menuItemName': 'Move Down',
                'hotkey': 'S', 
                'action': lambda: print('down') #commandMoveDown(Command)
            },
            {
                'menuItemName': 'Move Left',
                'hotkey': 'A', 
                'action': lambda: print('left') #commandMoveLeft(Command)
            },
            {	
                'menuItemName': 'Move Right',
                'hotkey': 'D', 
                'action': lambda: print('right') #commandMoveRight(Command)
            },
            {
                'menuItemName': 'Jump',
                'hotkey': 'Space', 
                'action': lambda: print('space') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'DisplayFPS',
                'hotkey': 'F1', 
                'action': lambda: print('left') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'SpecialAbility',
                'hotkey': 'E', 
                'action': lambda: print('E') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Grenade',
                'hotkey': 'Q', 
                'action': lambda: print('Q') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Shoot',
                'hotkey': 'Mouse1', 
                'action': lambda: print('M1') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Temp',
                'hotkey': 'T', 
                'action': lambda: print('T') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special1',
                'hotkey': 'spec1', 
                'action': lambda: print('spec1') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special2',
                'hotkey': 'spec2', 
                'action': lambda: print('spec2') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special3',
                'hotkey': 'spec3', 
                'action': lambda: print('spec3') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special4',
                'hotkey': 'spec4', 
                'action': lambda: print('spec4') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special5',
                'hotkey': 'Special5', 
                'action': lambda: print('Special5') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special6',
                'hotkey': 'Special6', 
                'action': lambda: print('Special6') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'Special7',
                'hotkey': 'Special', 
                'action': lambda: print('Special7') #commandMoveLeft(Command)
            },
            {
                'menuItemName': 'end',
                'hotkey': 'end', 
                'action': lambda: print('end') #commandMoveLeft(Command)
            },
        ]
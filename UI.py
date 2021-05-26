#Import Modules
try:
    import pygame
    from pygame.locals import *
    from pygame.math import Vector2
    import os
    import sys

    #My modules
    from Entity import Entity
    from GameModes import MenuGameMode, PlayGameMode, MessageGameMode, SettingsGameMode
    from GameState import GameState
    import Layers

except ImportError as error:
    print("Couldn't load module.")
    print(error)
    sys.exit(2)

#Center game window
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Main game class
class UserInterface():
    def __init__(self):
        self.gamestate = GameState()

        #Layers
        self.layers = [
            Layers.ArrayLayer('Assets\ground.png', self.gamestate.ground, self.gamestate),
            Layers.UnitLayer('Assets\\units.png', self.gamestate.units, self.gamestate.window),
            Layers.HUDLayer('Assets\ground.png', self.gamestate)
        ]

        #Init Pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.gamestate.windowCaption)
        
    def showLevel(self):
        #Init gameplay
        if self.currentGameMode is None:
            self.currentGameMode = PlayGameMode(UI)
            self.overlayGameMode = None
            self.activeGameMode = 'Play'
            
        #Resume gameplay
        else:
            self.overlayGameMode = None
            self.activeGameMode = 'Play'

    def showMessage(self):
        self.overlayGameMode = MessageGameMode(UI)
        self.activeGameMode = 'Overlay'
    
    def showMenu(self):
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'

    def showSettings(self):
        self.overlayGameMode = SettingsGameMode(UI)
        self.activeGameMode = 'Overlay'

    def quitGame(self): 
        self.gamestate.running = False
        
    def showFPS(self):
        #Draw font/text
        self.fontSurface = self.font.render("FPS: " + str(int(self.ui.clock.get_fps())), True, self.ui.white)  #Convert clock from a float to a int to round off decimal points
        self.ui.window.blit(self.fontSurface, (20, 20))

    def run(self, UI):
        #Set default gamemode to the menu
        self.currentGameMode = None 
        self.overlayGameMode = MenuGameMode(UI)
        self.activeGameMode = 'Overlay'

        #Main game loop
        while self.gamestate.running == True:
            #Determine what the current gamemode is and display an overlay if active
            if self.activeGameMode == 'Overlay':
                #Only process input from this game mode
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            
            elif self.currentGameMode is not None:
                self.currentGameMode.processInput()

                if self.gamestate.debug == True:
                    self.currentGameMode.update()

                else:
                    try:
                        self.currentGameMode.update()
                    except Exception as ex:
                        print('Error updating the current game mode')
                        self.currentGameMode = None
                        self.overlayGameMode = MenuGameMode(UI)
                        self.activeGameMode = 'Overlay'

            #Render 
            #Draw a black screen (clear the screen)
            self.gamestate.window.fill((0, 0, 0))

            #Render the play game mode if set
            if self.currentGameMode is not None:
                self.currentGameMode.render()
            
            #Render the Overlay if it is active
            if self.activeGameMode == 'Overlay':
                darkSurface = pygame.Surface(self.gamestate.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
                self.gamestate.window.blit(darkSurface, (0,0))
                self.overlayGameMode.render()

            #Draw graphics to the screen
            pygame.display.update()
            self.gamestate.clock.tick(self.gamestate.FPS)


UI = UserInterface()
UI.run(UI)

pygame.quit()
sys.exit()
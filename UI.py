#Import Modules
try:
    import pygame
    from pygame.locals import *
    from pygame.math import Vector2
    import os
    import sys

    #My modules
    from gamemodes import MenuGameMode, PlayGameMode, MessageGameMode, SettingsGameMode
    from gamestate import GameState

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
                try:
                    self.currentGameMode.update()
                except Exception as ex:
                    print('Error updating the current game mode')
                    print(ex)
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
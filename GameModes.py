import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

#My modules
import Entity
from Layers import Layer, ArrayLayer
    
class GameMode():
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self):
        raise NotImplementedError()

    def quitGame(self):
        pass

class MenuGameMode(GameMode):
    def __init__(self, UI):
        super().__init__() #Inherit all the properties and methods of the parent class
        self.ui = UI
        self.gamestate = UI.gamestate

        #Font
        self.fontSize = 40
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        
        #Create a list that contains all the menu options the user can choose from
        self.menuItems = [
            {
                'menuItemName': 'Tutorial Instructions',
                'action': lambda: self.ui.showMessage()
            },
            {
                'menuItemName': 'Level 1',
                'action': lambda: self.ui.showLevel()
            },
            {
                'menuItemName': 'Settings', 
                'action': lambda: self.ui.showSettings()
            },
            {
                'menuItemName': 'Quit', 
                'action': lambda: self.ui.quitGame()
            }
        ]

        self.currentMenuItem = 0
        self.menuItem = None
        self.menuCursor = pygame.font.SysFont('rubik', self.fontSize)
        self.menuName = "Tower Defense"

    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Exit the loop
                self.ui.quitGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_s:
                    if self.currentMenuItem < (len(self.menuItems) - 1):
                        self.currentMenuItem += 1
                elif event.key == pygame.K_RETURN:
                    #Gets the current menuitems action
                    self.menuItem = self.menuItems[self.currentMenuItem]

    def update(self):
        if self.menuItem is not None:
            try:
                #Execute the current menuitems Action lambda function
                self.menuItem['action']() 
                self.menuItem = None
            except Exception as ex:
                print(ex)

    def render(self):   
        #Computes where the x-pos should be to center the font surface
        def centerFontX(surface):
            offset = surface.get_width() // 2 #Take the length of the font divided by 2
            x = (self.gamestate.window.get_width() // 2) - offset #Take half the window width and the offset to determine where to draw

            return x

        # Initial y
        y = 50
        
        # Title
        surface = self.font.render(self.menuName, True, (200, 0, 0))
        x = centerFontX(surface)
        self.gamestate.window.blit(surface, (x, y))
        
        #Move down the y-pos to draw the menu items below the title
        y += (200 * surface.get_height()) // 100  
        
        #Iterate through each menuItem
        for item in self.menuItems:
            #Draw each menuItem to the screen
            surface = self.font.render(item['menuItemName'], True, (200, 0, 0))
            x = centerFontX(surface)
            self.gamestate.window.blit(surface, (x, y))
            
            #Cursor
            #Get the current index number
            index = self.menuItems.index(item)  
            
            #Render the cursor at the current MenuItem selected
            if index == self.currentMenuItem:
                surface = self.menuCursor.render("-->", True, (200, 0, 0))
                cursorX = x - (surface.get_width() + 10) 
                cursorY = y
                self.gamestate.window.blit(surface, (cursorX, cursorY))

            #Update y-pos so items are not overlaping
            y += (120 * surface.get_height()) // 100  

#---------------------------------------------------------------------------------------
class PlayGameMode(GameMode):
    def __init__(self, UI):
        self.ui = UI
        self.gamestate = UI.gamestate

    def processInput(self):
        # Event Handler
        for event in pygame.event.get():
            # If the user has clicked on the 'X' box, close the game
            if event.type == pygame.QUIT:
                self.gamestate.running = False
            # If the user has pressed down on the keyboard, handle the input
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.ui.showMenu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass #self.player1.processInput()  #Store the mouse click position
            else:
                pass

    def update(self):
        if len(self.gamestate.enemies) < 1:
            #Create a new enemy
            position = Vector2(64, 64)
            self.gamestate.enemies.append(Entity.Unit(position))
                
            #debug, remove later
            print(self.gamestate.enemies)

        for enemy in self.gamestate.enemies:
            enemy.update()

    def render(self):
        for layer in self.ui.layers:
            layer.render()

        

class MessageGameMode(GameMode):
    def __init__(self, UI):
        self.ui = UI

        self.fontSize = 24
        self.font = pygame.font.SysFont('rubik', self.fontSize)
        self.message = "You suck."

        self.returnToMenu = False
     
    def processInput(self):
        #Event handling 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE \
                or event.key == pygame.K_RETURN:
                    #Store the value to be updated later
                    self.returnToMenu = True

    def update(self):
        #Return to the menu
        if self.returnToMenu == True:
            self.ui.showMenu()
        
    def render(self):
        surface = self.font.render(self.message, True, (255, 0, 0))
        self.ui.window.blit(surface, (10, 200))

class SettingsGameMode(MenuGameMode):
    #Overrides the parent class
    def __init__(self, UI):
        #Inherits the methods and attributes of the parent class
        super().__init__(UI) 
        self.hotkeys = UI.gamestate.hotkeys
        self.gamestate = UI.gamestate
        
        self.hotkeysMaxLen = (len(self.hotkeys) - 1)
		
        self.indexOffset = 0
        self.indexMin = 0
        self.indexMax = None
        self.indexOffsetIncrease = None
        self.indexOffsetDecrease = None
        self.indexOffsetChanged = None
        
        self.cursorIndex = 0
        self.menuName = "Settings"
        self.menuItems = []
        self.menuItemsDisplayed = 0
        self.menuItemsDisplayedChanged = None
        self.moveMenu = None

        self.paddingBottom = 50

        #Determines how to execute the 3 main functions processInput, update, and render
        self.mode = "Show" #Show, Selection, or Confirmation
        self.modeChange = ""
        self.newHotkeyFlag = None
        self.saveHotkeysFlag = None

    def processInput(self):
        if self.mode == "Show":
            #Event handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Exit the loop
                    self.ui.quitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if self.currentMenuItem > self.indexMin:
                            self.moveMenu = 'up'
                            #If the User's cursor is halfway up the screen and the index offset is not 0 lower offset
                            if self.currentMenuItem < self.menuMiddle and self.indexOffset != 0:
                                self.indexOffsetDecrease = True
                            
                    elif event.key == pygame.K_s:
                        if self.currentMenuItem < self.indexMax:
                            self.moveMenu = 'down'
                            #If the User's cursor is halfway down the screen and the display list will not exceed the hotkeys master list length
                            if self.currentMenuItem > self.menuMiddle and (self.menuItemsDisplayed + self.indexOffset) <= self.hotkeysMaxLen:
                                self.indexOffsetIncrease = True
                            
                    elif event.key == pygame.K_RETURN:
                        #Get index, hotkey, and flag to change from show to selection
                        self.modeChange = "Sel"

                    elif event.key == K_ESCAPE:
                        if len(self.gamestate.rebindList) > 0:
                            #Ask the User to confirm or discard changes
                            self.modeChange = "Con"
                        else:
                            self.ui.showMenu()

        elif self.mode == "Selection":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ui.quitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.ui.showSettings()
                    
                    #If the user has selected a new hotkey, store it
                    else:
                        try: 
                            self.newHotkeyFlag = True
                            self.newHotkey = chr(event.key)
                        except Exception() as ex:
                            print("Error rebinding key selection")
                            self.ui.showSettings()
        
        elif self.mode == "Confirmation":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ui.quitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #Discard changes
                        self.gamestate.rebindList = []
                        self.ui.showMenu()
                    elif event.key == pygame.K_RETURN:
                        #Save changes
                        self.saveHotkeysFlag = True
                        

    def update(self):
        if self.modeChange is not None:
            if self.modeChange == "Sh":
                self.mode = "Show"
            elif self.modeChange == "Sel":
                self.mode = "Selection"
            elif self.modeChange == "Con":
                self.mode = "Confirmation"

        if self.mode == "Show":
            #Adjust indexOffset
            if self.indexOffsetIncrease == True:
                self.indexOffset += 1
                self.indexOffsetChanged = True

            elif self.indexOffsetDecrease == True:
                self.indexOffset -= 1
                self.indexOffsetChanged = True

            #User selection moves up
            #I check to make sure the index has not changed to prevent skipping a value. If the index 
            # changes and we move the menuItem the result is changing two positions instead of one.
            if self.moveMenu == 'up' and self.indexOffsetChanged != True:
                self.currentMenuItem -= 1

            #User selection moves down
            elif self.moveMenu == 'down' and self.indexOffsetChanged != True:
                self.currentMenuItem += 1

            #Clear values
            self.moveMenu = None
            self.indexOffsetIncrease = None
            self.indexOffsetDecrease = None

        elif self.mode == "Selection":
            if self.newHotkeyFlag == True:
                #Take User's input (key) and current index of hotkeys list
                Input = {"Index": self.cursorIndex, "Key": self.newHotkey}

		        #Store inputs
                self.gamestate.rebindList.append(Input)
                print(self.gamestate.rebindList)

                #Change flags
                self.modeChange = "Sh"
                self.newHotkeyFlag = False

        elif self.mode == "Confirmation":
            if self.saveHotkeysFlag == True:
                updatedHotkeysList = self.hotkeys.copy()
        
                for item in self.gamestate.rebindList:
                    userInput = item["Key"]
                    index = item["Index"]
                    
                    #Replace hotkey with new one
                    updatedHotkeysList[index]["hotkey"] = userInput
                
                #Clear list
                self.gamestate.rebindList = []
                self.gamestate.hotkeys = updatedHotkeysList

                self.ui.showMenu()
    
    def render(self): 
        paddingLeft = 20
        paddingRight = 500
        
        #
        def updateHeight(surface):
            updatedHeight = (120 * surface.get_height()) // 100
            return updatedHeight

        #Determines how many menu items can be displayed
        def itemsDisplayed(y):
            menuItemsDisplayed = 0
            for item in self.hotkeys:
                surface = self.font.render(item['menuItemName'], True, (200, 0, 0))

                #Update y-pos so items are not overlaping
                y += updateHeight(surface)

                menuItemsDisplayed += 1

                if y >= self.gamestate.windowSize.y - self.paddingBottom:
                    break

            return menuItemsDisplayed

        #Creates a list containing the menu items to display from the master hotkeys list
        def createDisplayList():
            displayList = []
            for index in range(self.menuItemsDisplayed):
                try:
                    displayList.append(self.hotkeys[index + self.indexOffset])
                except:
                    print("Index error in createDisplayList")
                
            return displayList

        #Computes where the x-pos should be to center the font surface
        def centerFontX(surface):
            offset = surface.get_width() // 2 #Take the length of the font divided by 2
            x = (self.gamestate.window.get_width() // 2) - offset #Take half the window width and the offset to determine where to draw

            return x

        if self.mode == "Show":
            # Initial y
            y = 50

            #Amount of pixels to space out text from the edges of the window
            padding = 20

            # Title
            surface = self.font.render(self.menuName, True, (200, 0, 0))
            x = centerFontX(surface)
            self.gamestate.window.blit(surface, (x, y))

            y += (200 * surface.get_height()) // 100  #Change the y-pos to draw the menu items

            #If this is the first iteration or the screen size has been changed, recreate the list 
            if self.menuItemsDisplayedChanged == None or self.menuItemsDisplayedChanged == True:
                self.menuItemsDisplayed = itemsDisplayed(y)
                self.menuMiddle = round(self.menuItemsDisplayed / 2)
                self.menuItemsDisplayedChanged = False

            #If this is the first iteration or the index offset has been changed, recreate the list 
            if self.indexOffsetChanged == None or self.indexOffsetChanged == True:
                self.menuItems = createDisplayList()
                self.indexMax = (len(self.menuItems) - 1)
                self.indexOffsetChanged = False

            #Render list
            for item in self.menuItems:         
                #Draw each menuItem to the screen
                surface = self.font.render(item['menuItemName'], True, (200, 0, 0))
                x = paddingLeft
                self.gamestate.window.blit(surface, (x, y))

                #Draw each hotkey to the screen
                surface = self.font.render(item['hotkey'], True, (200, 0, 0))
                x = paddingRight
                self.gamestate.window.blit(surface, (x, y))
                
                #Cursor
                index = self.menuItems.index(item)

                #Render the cursor at the current MenuItem selected
                if index == self.currentMenuItem:
                    surface = self.menuCursor.render("-->", True, (200, 0, 0))
                    cursorX = x - (surface.get_width() + 10) 
                    cursorY = y
                    self.gamestate.window.blit(surface, (cursorX, cursorY))
                    self.cursorIndex = index + self.indexOffset

                #Update y-pos so items are not overlaping
                y += updateHeight(surface)

        elif self.mode == "Selection":
            y = 50

            # Title
            surface = self.font.render("Select new hotkey, Esc to cancel.", True, (200, 0, 0))
            x = centerFontX(surface)
            self.gamestate.window.blit(surface, (x, y))

            y += (200 * surface.get_height()) // 100

            #Draw current selected menuItem
            surface = self.font.render(self.menuItems[self.currentMenuItem]['menuItemName'], True, (200, 0, 0))
            x = paddingLeft
            self.gamestate.window.blit(surface, (x, y))

            surface = self.font.render(self.menuItems[self.currentMenuItem]['hotkey'], True, (200, 0, 0))
            x = paddingRight
            self.gamestate.window.blit(surface, (x, y))

        elif self.mode == "Confirmation":
            y = 50

            # Title
            surface = self.font.render("Press enter to confirm, Esc to discard changes.", True, (200, 0, 0))
            x = centerFontX(surface)
            self.gamestate.window.blit(surface, (x, y))
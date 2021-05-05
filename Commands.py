import pygame
import random
from pygame.locals import *
from pygame.math import Vector2

#My modules
from GameState import GameState

class Command():
    def __init__(self):
        pass

    def run(self):
        pass	

class RebindKeysCommand(Command):
	def __init__(self, hotkeyList, rebindList):
		updatedHotkeysList = hotkeyList.copy()
	
	def run(self):
		for item in rebindList:
			userInput = item["key"]
			index = item["Index"]
			
			#Replace hotkey with new one
			updatedHotkeysList[index]["hotkey"] = userInput
		
		
		#Clear list
		rebindList = []	
		
		#This returns the values as a tuple
		return updatedHotkeysList, rebindList
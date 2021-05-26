class Command():
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError()

class MoveCommand():
    def __init__(self, unit, move, gamestate):
        self.unit = unit
        self.gs = gamestate
        self.newPos = self.unit.pos + move  # Potential new position

    def run(self):
        # Check if the unit would go beyond the world bounds
        if self.newPos.x < 0 or self.newPos.x > self.gs.windowSize.x \
                or self.newPos.y < 0 or self.newPos.y > self.gs.windowSize.y:
            # Unit out of world bounds
            return

        # Check if the position is occupied by another unit
        for other in self.gs.units:
            if self.newPos == other.pos:
                return

        # Passed all checks, update position
        self.unit.pos = self.newPos


'''
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
		return updatedHotkeysList, rebindList'''

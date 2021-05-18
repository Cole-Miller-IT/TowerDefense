# TowerDefense
'''
Project: tower Defence game
Author: Cole Miller
Date: May, 2021 - current date
Help/Resources used: 
https://www.patternsgameprog.com/series/                    #Big help with structuring the game 
https://www.pygame.org/docs/								#Documentation for the pygame module
https://www.w3schools.com/python/							#Useful python tutorials 

Goals:
-Setup Python environment                                   COMPLETED
-Structure game, and create the first window                COMPLETED
-Implement re-bindable hotkeys menu                        	COMPLETED
-Add hotkeys to the play gamemode class                     
-Clean up settingsMenuGamemode class
-Clean up UI/Array Layer, make more concise 				COMPLETED
-Draw BackGround layer to the playgamemode                  COMPLETED
-Add the enemy                                              COMPLETED
-Clean up renderUnit method of the layer class				COMPLETED
-Implement MessageGameMode
-Create the HUD layer
-Create a spritesheet for the ground with roads
-Move hotkeys list to a txt file to save data 				



#Commands to help configure VS Code with Python using a virtual environment
First, run the command below in the terminal window to create a python virtual environment
py -m venv venv  

Second, switch the python interpreter to use this new interpreter. Close and open a new terminal, you should see (venv) before the path to this game.
Press ctrl + shift + p, "Python: Select interpreter", and select the new virtual environment (should contain "venv"

Next, install the latest version of pip
py -m pip install --upgrade pip

Next, install any modules you may need such as the pygame module.
py -m pip install pygame  


Troubleshooting:
Incase you recieve a error related to this problem, run this in Powershell.
"terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "Bypass"]  
'''
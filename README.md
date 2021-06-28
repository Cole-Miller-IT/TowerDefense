# TowerDefense
'''
Project: 	Tower Defence game
Author: 	Cole Miller
Date: 		May, 2021 - current date
Help/Resources used: 
https://www.patternsgameprog.com/series/                    #Big help with structuring the game 
https://www.pygame.org/docs/								#Documentation for the pygame module
https://www.w3schools.com/python/							#Useful python tutorials 
https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame  #Debugging surface rotation
https://www.reddit.com/r/pygame/comments/49n8dy/why_out_of_memory/                                   #Debugging surface rotation
https://www.letsdevelopgames.com/2020/10/entity-component-system-in-python-code.html	#Entity Component system

Goals:
-Setup Python environment                                   COMPLETED
-Structure game, and create the first window                COMPLETED
-Implement re-bindable hotkeys menu                        	COMPLETED
-Add hotkeys to the play gamemode class                     
-Clean up UI/Array Layer, make more concise 				COMPLETED
-Draw BackGround layer to the playgamemode                  COMPLETED
-Add the enemy                                              COMPLETED
-Clean up renderUnit method of the layer class				COMPLETED
-Implement MessageGameMode
-Create the HUD layer
-Create a spritesheet for the ground with roads				COMPLETED
-Create a spritesheet for units                             COMPLETED
-Move hotkeys list to a txt file to save data 			
-Implement entity component system overhaul			
 -Add texture rotation                                      COMPLETED
 -Implement Targeting system								COMPLETED
 -Create dependency tree diagram
 -Use txt file to load map tile data (ex. where roads are)
 -Implement movement system
 -Clean up rebindable hotkeys menu (constant half of the screen width) 
 -Add unit collision to the move system
 -Create 2 maps using Tiled software
 -Add more error checking for importing modules, 			COMPLETED
 -Change prepareSurfaces to repeat if multiple textureobjects COMPLETED
 are present, if not just run once.
 -Make a texture system class for handling entity textures	COMPLETED
 -implement component error checking, finding what 
 components are missing from the functions
 -add observer/observables classes https://www.protechtraining.com/blog/post/tutorial-the-observer-pattern-in-python-879
-Add tutorial level/message


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

If pylance throws up an error Unident not matching or inconsistent use of tabs . Fix: ctrl + A all the code, right click, and select format document. Lord help me,a tab vs. 4 spaces.
'''
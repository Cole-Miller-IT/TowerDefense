# TowerDefense
'''
Project: tower Defence game
Author: Cole Miller
Date: May, 2021 - current date
Help/Resources used: 
https://www.patternsgameprog.com/series/                    #Big help with structuring the game 

Goals:
-Setup Python environment                                   COMPLETED
-Structure game, and create the first window                COMPLETED
-Implement re-bindable hotkeys                              COMPLETED
-Add hotkeys to the play gamemode class                     
-Clean up settingsMenuGamemode class
-Draw BackGround layer to the playgamemode                  COMPLETED

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
Incase you recieve a error related to this problem use this in Powershell.
"terminal.integrated.shellArgs.windows": ["-ExecutionPolicy", "Bypass"]  #Used to allow 
'''
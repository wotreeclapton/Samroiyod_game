#Game option/settings
import os
from contextlib import contextmanager

@contextmanager
def change_dir(destination): #change directory function
	try:
		cwd = os.getcwd()
		os.chdir(destination)
		yield
	finally:
		os.chdir(cwd)

COMX = 380
COMY = 85
SCREENWIDTH = 800
SCREENHEIGHT = 780
FPS = 60

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED =(255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

POWERUP_TIME = 10000
#MOVE_DELAY = 550


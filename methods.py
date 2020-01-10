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







	# def play_mob_movesound(self):
	# 	if len(self.mobs) + len(self.Bmobs) > 0 and self.player.alive():
	# 		sound_delay = self.move_delay
	# 		if sound_delay < 150:
	# 			sound_delay = 150
	# 		now = pg.time.get_ticks()
	# 		if now - self.sound_last_update >= sound_delay:
	# 			self.sound_last_update = now
	# 			if self.sound:
	# 				self.enemy_sounds[3].play()
	# 				self.sound = False	
	# 			else:
	# 				self.enemy_sounds[0].play()	
	# 				self.sound = True

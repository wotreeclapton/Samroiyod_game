#! python 3
'''
SAMROIYOD GAME METHODS developed by Mr Steven J walden
    Nov. 2020
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND
[See License.txt file]
'''

import os
from contextlib import contextmanager
import pygame as pg

@contextmanager
def change_dir(destination): #change directory function
	try:
		cwd = os.getcwd()
		os.chdir(destination)
		yield
	finally:
		os.chdir(cwd)

def write_high_score(score): #write the high score to BAT file
	with change_dir('resources'):
		with open('high_score.bat', 'w') as h_score_file:
			h_score_file.write(score)

def draw_text(surf, text, size, x, y, pos): #write text to the surface
	font_type = ['HARLOWSI.ttf','OCRAEXT.ttf']
	with change_dir('img'):
		font = pg.font.Font(font_type[pos], size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	if pos == 1:
		surf.blit(text_surface, ((x - text_rect.width / 2) ,y))
	else:
		surf.blit(text_surface, (x,y))

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

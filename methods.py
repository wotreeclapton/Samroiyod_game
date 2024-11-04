'''
SAMROIYOD GAME METHODS developed by Mr Steven J walden
    Nov. 2020
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND
[See License.txt file]
'''

import pygame as pg
import constants as const
from os import path

def draw_text(surf, text, size, x, y): #write text to the surface
	# font_types = [path.join(const.RESOURCES_FOLDER, const.HARLOW_FONT), path.join(const.RESOURCES_FOLDER, const.OCRA_FONT)]
	font = pg.font.Font(path.join(const.RESOURCES_FOLDER, const.OCRA_FONT), size)
	# font = pg.font.Font(font_types[1], size)
	text_surface = font.render(text, True, const.WHITE)
	# text_rect = text_surface.get_rect()
	# if font_type == 1:
	# 	surf.blit(text_surface, ((x - text_rect.width / 2) ,y))
	# else:
	surf.blit(text_surface, (x,y))

def screen_location(wn, avail_geom):
	#Set the screen location of a gui [wn = passed gui object, avail_geom = available screen size]
	#ag = QDesktopWidget().availableGeometry()
	#sg = QDesktopWidget().screenGeometry()

	widget = wn.geometry()
	x = avail_geom.width() / 2 - widget.width() / 2
	y = avail_geom.height() / 2 - widget.height() / 2
	wn.move(x, y)

def draw_shields(surf, x, y, shield_amm):
	if shield_amm <= 0:
		shield_amm = 0
	bar_length = 100
	bar_height = 13
	fill = (shield_amm / 100) * bar_length
	outline_rect = pg.Rect(x, y, bar_length, bar_height)
	fill_rect = pg.Rect(x, y, fill, bar_height)
	pg.draw.rect(surf, const.GREEN, fill_rect)
	pg.draw.rect(surf, const.WHITE, outline_rect, 1)

def draw_lives(surf, x, y, player):
	player_image_resized = pg.transform.scale(player.image, (20, 20))
	for i in range(player.lives):
		surf.blit(player_image_resized, (x + (i * 25), y))

def new_high_score_check(game):
	# play high score sound
	if game.number_of_players == 2:
		if not game.played_high_score_sound and game.p2score > game.orig_high_score:
			game.high_score_sound.play()
			game.played_high_score_sound = True
	if not game.played_high_score_sound and game.p1score > game.orig_high_score:
		game.high_score_sound.play()
		game.played_high_score_sound = True


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

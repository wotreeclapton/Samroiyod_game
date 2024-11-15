'''
	SAMROIYOD GAME LEVEL CHange developed by Mr Steven J walden
		Nov. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	Some of the sounds in this project were created by David McKee (ViRiX) soundcloud.com/virix

	[See License.txt file]
'''

import pygame as pg
import constants as const
from game_state import GameState
from sprites import LevelUpPlayer1, LevelUpPlayer2


class LevelChange(GameState):
	def __init__(self, game):
		super().__init__(game)
		# In game player sprite status and collision checks class
		self.game = game
		self.player_moved = False
		self.load_images()

	def load_images(self):
		self.background = self.game.resource_manager.get_image("game_screen") #Change this to a different screen later
		self.background_rect = self.background.get_rect()
		self.level_mobs = pg.sprite.Group()

		self.player1_level_image = LevelUpPlayer1(self.game)
		self.player2_level_image = LevelUpPlayer2(self.game)

		self.level_mobs.add(self.player1_level_image)
		self.level_mobs.add(self.player2_level_image)

	def enter(self, xpos_data=None):
		if len(xpos_data) < 2:
			if self.game.player1.alive():
				self.player1_level_image.rect.centerx = xpos_data[0] if xpos_data else []
			else:
				self.player2_level_image.rect.centerx = xpos_data[0] if xpos_data else []
		else:
			self.player1_level_image.rect.centerx = xpos_data[0] if xpos_data else []
			self.player2_level_image.rect.centerx = xpos_data[1] if xpos_data else []

		if len(self.game.player_group) > 1:
			self.player1_level_image.end_poss = const.SCREENWIDTH/3
			self.player2_level_image.end_poss = const.SCREENWIDTH/3 * 2
        
	def handle_events(self, events):
		for event in events:
			if event.type == pg.QUIT:
				self.game.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.game.quit()
				# if event.key == pg.K_p:
				# 	self.game.change_state(self.game.states["pause"])
			# try:
			# 	if self.joystick.get_button(9):
			# 		self.pause = False
			# except AttributeError:
			# 	pass

	def update(self):
		self.level_mobs.update()

	def draw(self):
		self.game.win.blit(self.background, self.background_rect)
		self.level_mobs.draw(self.game.win)
		pg.display.update()

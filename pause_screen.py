"""
	SAMROIYOD GAME PAUSE CONTROL developed by Mr Steven J walden
		September. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	[See License.txt file]

"""

import pygame as pg
import constants as const
from game_state import GameState

class PauseScreen(GameState):
	def __init__(self, game):
		super().__init__(game)
		#Pause screen class to handle in game pausing
		self.game = game
		self.pause_mobs = pg.sprite.Group()
		self.pause_img = PauseQuest(self.game, const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2)
		self.pause_mobs.add(self.pause_img)
		self.background = self.game.resource_manager.get_image("game_screen")
		self.background_rect = self.background.get_rect()

	def handle_events(self, events):
		for event in events:
			if event.type == pg.QUIT:
				self.game.quit()			
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.game.quit()
				if event.key == pg.K_p:
					if self.game.boss is not None:
						self.game.boss.channel.unpause()
					self.game.change_state("play")
			try:
				if self.game.joystick1.get_button(9) or self.game.joystick2.get_button(7):
					if self.game.boss is not None:
						self.game.boss.channel.unpause()
					self.game.change_state("play")
			except AttributeError:
				pass

	def update(self):
		self.pause_mobs.update()

	def draw(self):
		self.game.win.blit(self.background, self.background_rect)#
		self.pause_mobs.draw(self.game.win)
		pg.display.update()


class PauseQuest(pg.sprite.Sprite):
	# class to handle flashing start mob
	def __init__(self, game, x, y):
		super().__init__()
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("pause_image")
		self.original_image = self.image  # Store the original image
		self.rect = self.image.get_rect()
		self.transparent_image = pg.Surface(
                    (self.rect.width, self.rect.height), pg.SRCALPHA)
		self.transparent_image.fill((0, 0, 0, 0))  # Transparent surface
		self.rect.centerx = x
		self.rect.y = y
		self.flash_interval = 500
		self.last_flash_time = pg.time.get_ticks()
		self.visible = True

	def update(self):
		current_time = pg.time.get_ticks()
		if current_time - self.last_flash_time >= self.flash_interval:
			self.visible = not self.visible
			self.last_flash_time = current_time

		if self.visible:
			self.image = self.original_image
		else:
			self.image = self.transparent_image

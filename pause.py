"""
	SAMROIYOD GAME PAUSE CONTROL developed by Mr Steven J walden
		September. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	[See License.txt file]

"""

import pygame as pg
import constants as const

class Pause:
	def __init__(self, game) -> None:
		#Pause screen class to handle in game pausing
		self.game = game
		self.pause_mobs = pg.sprite.Group()
		self.pause_img = PauseQuest(self.game, const.SCREENWIDTH / 2, const.SCREENHEIGHT / 2)
		self.pause_mobs.add(self.pause_img)
		self.pause = True

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_p:
					self.pause = False
			# try:
			# 	if self.joystick.get_button(9):
			# 		self.pause = False
			# except AttributeError:
			# 	pass

	def update(self):
		self.pause_mobs.update()

	def draw(self):
		self.game.win.blit(self.game.background, self.game.background_rect)#
		self.pause_mobs.draw(self.game.win)
		pg.display.update()

	def show(self):
		while self.pause:
			self.handle_events()
			self.update()
			self.draw()

			
			# display pause writing
			# if count <= 300:
				# self.win.blit(self.paused_img, (const.SCREENWIDTH / 2 -
				#               self.paused_img_rect.width / 2, const.SCREENHEIGHT / 2))
				# self.draw_text(surf=self.win, text="Paused", size=68, x=400, y=const.SCREENHEIGHT / 2, pos=1)
			# if count >= 600:
			# 	count = 0
			# count += 1
			
			# unpause


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

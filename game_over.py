"""
	SAMROIYOD GAME OVER SCREEN developed by Mr Steven J walden
		September. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	[See License.txt file]

"""

import pygame as pg
from resource_manager import write_high_score
from game_state import GameState


class GameOverScreen(GameState):
	def __init__(self, game):
		super().__init__(game)
		# Game over Screen class to handle all start options
		self.game = game

		self.load_resources()
		# save high score
		write_high_score(str(self.game.high_score))

	def load_resources(self):
		self.background = self.game.resource_manager.get_image("gameover_screen")
		self.background_rect = self.background.get_rect()

	def handle_events(self, events):
		# self.clock.tick(const.FPS)
		for event in events:  # exit loop
			if event.type == pg.QUIT:
				self.game.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.game.quit()
				else:
					self.game.change_state("start")

			# if event.type == pg.KEYUP:
			# 	if event.key == pg.K_y:  # Continue
			# 		self.waiting = False
			# 		self.start_screen_pass = True
			# try:
			# 	for joystick in self.joystick_list:
			# 		# Select button to return to start screen
			# 		if self.joystick.get_button(8) or self.joystick.get_button(6):
			# 			self.waiting = False
			# 		# Play button to continue
			# 		if self.joystick.get_button(9) or self.joystick.get_button(7):
			# 			self.waiting = False
			# 			self.start_screen_pass = True
			# except AttributeError:
			# 			pass
	
	def update(self):
		pg.display.update()

	def draw(self):
		# Game over/continue screen
		self.game.win.blit(self.background, self.background_rect)
		# Draw score
		# if self.number_of_players == 2:
		# 	meth.draw_text(surf=self.win, text=f"Player 2: {self.p2score}", size=38, x=400, y=535, pos=1)
		# 	meth.draw_text(surf=self.win, text=f"Player 1: {self.p1score}", size=38, x=400, y=471, pos=1)
		# 	pg.mixer.music.fadeout(2000)


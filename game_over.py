"""
	SAMROIYOD GAME OVER SCREEN developed by Mr Steven J walden
		September. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	[See License.txt file]

"""

import pygame as pg
from resource_manager import write_high_score
from game_state import GameState
from methods import draw_text


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
				self._handle_keydown(event)

		self.check_joystick()

	def	_handle_keydown(self, event):
		if event.key == pg.K_ESCAPE:
			self.game.quit()
		else:
			self.game.change_state("start")

	def	check_joystick(self):
		try:
			if self.game.joystick1:
				# Select button to return to start screen
				if self.game.joystick_handler1.is_button_pressed(8) or self.game.joystick2.get_button(6):
					self.game.quit()
				# Play button to continue
				if self.game.joystick_handler1.is_button_pressed(9) or self.game.joystick2.get_button(7):
					self.game.change_state("start")

			if self.game.joystick2:
				# Select button to return to start screen
				if self.game.joystick_handler2.is_button_pressed(6):
					self.game.quit()
				# Play button to continue
				if self.game.joystick_handler2.is_button_pressed(7):
					self.game.change_state("start")

		except AttributeError as e:
			print(f"Joystick error: {e}")

	def update(self):
		pg.display.update()

	def draw(self):
		# Game over/continue screen
		self.game.win.blit(self.background, self.background_rect)
		# Draw score
		if all(item is True for item in self.game.players):
			draw_text(surf=self.win, text=f"Player 2: {self.p2score}", size=38, x=400, y=535, pos=1)
			draw_text(surf=self.win, text=f"Player 1: {self.p1score}", size=38, x=400, y=471, pos=1)
		else:
			draw_text(surf=self.win, text=f"Player 1: {self.p1score}", size=38, x=400, y=471, pos=1)

			pg.mixer.music.fadeout(2000)


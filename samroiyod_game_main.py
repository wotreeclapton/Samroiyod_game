'''
SAMROIYOD GAME LAUNCHER developed by Mr Steven J walden
    Nov. 2020
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

Some of the sounds in this project were created by David McKee (ViRiX) soundcloud.com/virix

[See License.txt file]
'''
'''
enemy move down check
level up clear bullets and bosses
Joystick prob
powerup rewards
double points
make bonus level
level bosses
create a delay and message on level change
hyperspace
'''
from os import environ, path
import sys
import random
import pygame as pg

import constants as const
from start import StartScreen
from play_screen import PlayScreen
from game_over import GameOverScreen
from pause_screen import PauseScreen
from level_change import LevelChange
from sprites import Player1, Player2
# from hyperspace import hyperspace
from resource_manager import ResourceManager
from game_checks import CheckEnemy, CheckPlayer, CheckLevel

class Game(object):
	def __init__(self):
		#Initialize game window, etc
		self.clock = pg.time.Clock()
		self.resource_manager = ResourceManager()

		#Define game variables
		self.running = True
		self.rand_delay = random.randrange(8400,12000)
		self.last_update = pg.time.get_ticks()
		self.boss_last_update = pg.time.get_ticks()
		self.sound_last_update = pg.time.get_ticks()
		self.sound = True
		self.game_level = 1
		self.number_of_players = 0
		self.boss = None #Created first for pause game check
		self.played_high_score_sound = False
		self.high_score = 0
		self.orig_high_score = 0
		self.enemy = None
		self.bigenemy = None

		self._initialize_game()

	def _initialize_game(self):
        # Setup game window, logo, etc.
		pg.mixer.pre_init(44100, -16, 1, 512)
		environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (const.COMX, const.COMY)
		pg.init()
		self.win = pg.display.set_mode((const.SCREENWIDTH, const.SCREENHEIGHT))
		self.initialize_joysticks()
		self.load_resources()

	def initialize_joysticks(self):
		#Initialize available joysticks and handle errors during setup.
		try:
			total_joysticks = pg.joystick.get_count()
			self.joystick_list = []

			for i in range(total_joysticks):
				try:
					current_joystick = pg.joystick.Joystick(i)
					current_joystick.init()
					self.joystick_list.append(current_joystick)
				except pg.error as e:
					print(f"Joystick {i} failed to initialize: {e}")

			# Assign joystick attributes if available
			if total_joysticks >= 1:
				self.joystick1 = self.joystick_list[0]
			if total_joysticks >= 2:
				self.joystick2 = self.joystick_list[1]

			print(f"{total_joysticks} joystick(s) initialized successfully.")
		except Exception as e:
			print(f"Error during joystick initialization: {e}")

	def load_resources(self):
		try:
			self.logo = pg.image.load(path.join(const.IMAGE_FOLDER, "eplogo_small.png"))
		except pg.error as e:
			print(f"Failed to load logo: {e}")
		pg.display.set_icon(self.logo)
		pg.display.set_caption(f"{const.GAMENAME} {const.__VERSION__}")
		self.resource_manager.load_all_resources()

	def change_state(self, new_state_key, **kwargs):
		#Switch to a new game state.
		self.state = self.states[new_state_key]
		if kwargs:
			self.state.enter(**kwargs)

	def initialize_players(self):
		# choose 1 or 2 players
		if self.number_of_players == 2:
			self.p2score = 0
			self.player2 = Player2(xpos=(const.SCREENWIDTH / 3)*2, game=g)
			self.player_group.add(self.player2)
			self.all_sprites.add(self.player2)
			self.player1 = Player1(xpos=const.SCREENWIDTH / 3, game=g)
		else:
			self.player1 = Player1(xpos=const.SCREENWIDTH / 2, game=g)
			self.p1score = 0
			self.player_group.add(self.player1)
			self.all_sprites.add(self.player1)

	def initialize_sprite_groups(self):
		self.all_sprites = pg.sprite.Group()
		self.player_group = pg.sprite.Group()
		self.player1_bullets = pg.sprite.Group()
		self.player2_bullets = pg.sprite.Group()
		self.mob_bullets = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.Bmobs = pg.sprite.Group()
		self.bosses = pg.sprite.Group()
		self.powerups = pg.sprite.Group()
		
	def new(self):
		#Start a new game
		self.initialize_sprite_groups()
		self.initialize_players()

		#Create instances of game checks
		self.enemy_checks = CheckEnemy(g)
		self.player_checks = CheckPlayer(g)
		self.level_checks = CheckLevel(g)
		
        # Pre-create all states
		self.states = {
			"start": StartScreen(g),
            "play": PlayScreen(g),
            "gameover": GameOverScreen(g),
            "pause": PauseScreen(g),
			"level_change": LevelChange(g)
            }
		
		# State management
		self.state = self.states["start"]  # Set initial state

		pg.mixer.music.load(self.resource_manager.get_music("game_music"))
		pg.mixer.music.set_volume(0.2)
		pg.mixer.music.play(loops=-1)

		self.run()

	def quit(self):
		"""Quit the game."""
		self.running = False

	def run(self):
        # Main game loop
		while self.running:
			events = pg.event.get()
			self.state.handle_events(events)
			self.state.update()
			self.state.draw()
			self.clock.tick(const.FPS)

		pg.quit()

print(sys.executable)

if __name__ == '__main__':
	print("Author:", const.__AUTHOR__)
	print("App version:", const.__VERSION__)

	g = Game()
	g.new()
"""
	SAMROIYOD GAME START SCREEN developed by Mr Steven J walden
		September. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	[See License.txt file]

"""
import pygame as pg
import constants as const
from sprites import StartMob


class StartScreen:
	def __init__(self, game):
		#Start Screen class to handle all start options
		self.game = game
		self.running = True
		# self.number_of_players = 0
		self.player1 = False
		self.player2 = False
		self.players = [False, False]
		self.player_checked = False
		self.load_resources()

	def load_resources(self):
		# set music
		pg.mixer.music.load(self.game.resource_manager.get_music("start_screen_music"))
		pg.mixer.music.set_volume(const.MUSIC_VOLUME)
		pg.mixer.music.play(loops=-1)

		# Load images
		self.background = self.game.resource_manager.get_image("start_screen")
		self.background_rect = self.background.get_rect()
		self.player1_start_img = self.game.resource_manager.get_sprite_image("player1_start_images")
		self.player2_start_img = self.game.resource_manager.get_sprite_image("player2_start_images")

		#create all instance of mobs
		self.start_mobs = pg.sprite.Group()
		self.start_sam_enemy = StartMob(187, 471, "samroy", 100,  self.game)
		self.start_mobs.add(self.start_sam_enemy)

		self.start_ep_enemy = StartMob(319, 471, "ep", 50,  self.game)
		self.start_mobs.add(self.start_ep_enemy)

		self.player1_button = StartButtons(self.game, 1, const.START_BUTTON1_X)
		self.player2_button = StartButtons(self.game, 2, const.START_BUTTON2_X)
		self.start_mobs.add(self.player1_button)
		self.start_mobs.add(self.player2_button)

	def handle_events(self):
		#Handles player input, including keyboard and quitting events.
		for event in pg.event.get():  # exit loop
			if event.type == pg.QUIT:
				self.game.game_on = False
				self.running = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.running = False
					self.game.game_on = False
				elif event.key in {pg.K_1, pg.K_2, pg.K_RETURN}:
					self.check_keyboard_inputs(event)
				
		# self.check_joystick()

		if self.game.number_of_players > 0:
			if not self.player_checked:
				self.player_checked = True #set flag to prevent multiple checks
				self.start_quest = StartQuest(self.game, const.SCREENWIDTH / 2, 330)
				self.start_mobs.add(self.start_quest)
				
	def check_keyboard_inputs(self, event):
		#Checks player choice input
		if event.key == pg.K_1:
			if self.game.number_of_players != 1:
				self.game.number_of_players = 1
				self.players[0] = True

		if event.key == pg.K_2:
			if self.game.number_of_players != 2:
				self.game.number_of_players = 2
				self.players[0] = True
				self.players[1] = True

		#code to start game after player select
		if event.key == pg.K_RETURN:
			if self.game.number_of_players > 0:
				self.running = False
				self.start_mobs.empty()

	# def check_joystick(self):
	# 	try:
	# 		if self.joystick1.get_button(9):  # Player 1 start button
	# 			if self.number_of_players == 1:
	# 				self.number_of_players = 0
	# 				self.p1 = False
	# 			elif self.number_of_players == 2:
	# 				self.p1 = True
	# 			elif self.number_of_players == 2 and self.p1 == True:
	# 				self.p1 = False
	# 			else:
	# 				self.number_of_players = 1
	# 				self.count = 0
	# 				self.p1 = True
					
	# 		# Player 2 start button
	# 		if self.joystick2.get_button(7) and self.player_buttons.image == self.resource_manager.get_sprite_image("start_button2"):
	# 			if self.number_of_players == 2:
	# 				self.number_of_players = 1
	# 				self.p2 = False
	# 			else:
	# 				self.number_of_players = 2
	# 				self.p2 = True
	# 				self.count = 0
	# 		if self.joystick1.get_button(2) or self.joystick2.get_button(0):
	# 			if self.player_buttons.image == self.resource_manager.get_sprite_image("start_button2") and self.p1 == True and self.p2 == True or self.player_buttons.image == self.resource_manager.get_sprite_image("start_button1") and self.p1 == True:
	# 				s = False
	# 				self.start_mobs.empty()
	# 	except AttributeError:
	# 		pass

	def update(self):
		self.start_mobs.update()

	def draw(self):
		self.game.win.blit(self.background, self.background_rect)
		# draw player images
		if self.game.number_of_players == 2 and self.players[0]:
			self.game.win.blit(self.player1_start_img, (46, 607))
			self.game.win.blit(self.player2_start_img, (506, 607))
		if self.game.number_of_players == 2 and not self.players[0]:
			self.game.win.blit(self.player2_start_img, (506, 607))
		if self.game.number_of_players == 1 and self.players[0]:
			self.game.win.blit(self.player1_start_img, (46, 607))

		self.start_mobs.draw(self.game.win)
		pg.display.update()

	def show(self):
		while self.running:
			self.handle_events()
			self.update()
			self.draw()


class StartQuest(pg.sprite.Sprite):
	#class to handle flashing start mob
	def __init__(self, game, x, y):
		super().__init__()
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("press_to_start")
		self.original_image = self.image  # Store the original image
		self.rect = self.image.get_rect()
		self.transparent_image = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
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


class StartButtons(pg.sprite.Sprite):
	"""docstring for StartButtons"""
	def __init__(self, game, button_type, x):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image_type = button_type
		self.image = f"{self.image_type}up_button_small"
		self.image = self.game.resource_manager.get_sprite_image(self.image)
		self.rect = self.image.get_rect()
		self.x = x
		self.rect.center = (self.x, 710)

	def update(self):
		keystate = pg.key.get_pressed()
		if keystate[pg.K_1]:
			if self.image_type == 1:
				self.image = self.game.resource_manager.get_sprite_image(f"{self.image_type}up_button_large")
			else:
				self.image = self.game.resource_manager.get_sprite_image(f"{self.image_type}up_button_small")
		if keystate[pg.K_2]:
			if self.image_type == 2:
				self.image = self.game.resource_manager.get_sprite_image(f"{self.image_type}up_button_large")
			else:
				self.image = self.game.resource_manager.get_sprite_image(f"{self.image_type}up_button_small")

		# try:
		# 	if self.game.joystick1.get_axis(0) > 0 or self.game.joystick2.get_axis(0) > 0:
		# 		if self.image == self.game.resource_manager.get_sprite_image("start_button1"):
		# 			self.image = self.game.resource_manager.get_sprite_image("start_button2")
		# 	if self.game.joystick1.get_axis(0) == -1 or self.game.joystick2.get_axis(0) == -1:
		# 		if self.image == self.game.resource_manager.get_sprite_image("start_button2"):
		# 			self.image = self.game.resource_manager.get_sprite_image("start_button1")
		# except AttributeError:
		# 	pass

		self.rect = self.image.get_rect()
		self.rect.center = (self.x, 710)

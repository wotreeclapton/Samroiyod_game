"""
	SAMROIYOD GAME START SCREEN developed by Mr Steven J walden
		September. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	[See License.txt file]

"""
import pygame as pg
import constants as const
from sprites import StartMob, FlashingSprite
from game_state import GameState

class StartScreen(GameState):
	def __init__(self, game):
		super().__init__(game)
		#Start Screen class to handle all start options
		self.game = game
		self.running = True
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

	def handle_events(self, events):
		#Handles player input, including keyboard and quitting events.
		for event in events:  # exit loop
			if event.type == pg.QUIT:
				self.game.quit()
			elif event.type == pg.KEYDOWN:
				self._handle_keydown(event)

		if self.game.joystick1:
			self.check_joystick1()
		if self.game.joystick2:
			self.check_joystick2()

		if any(self.game.players):
			if not self.player_checked:
				self.player_checked = True #set flag to prevent multiple checks
				self.start_quest = StartQuest(self.game, const.SCREENWIDTH / 2, 330)
				self.start_mobs.add(self.start_quest)
				
	def _handle_keydown(self, event):
		if event.key == pg.K_ESCAPE:
			self.game.quit()
		elif event.key in {pg.K_1, pg.K_2, pg.K_RETURN}:
			self.check_keyboard_inputs(event)

	def check_keyboard_inputs(self, event):
		#Checks player choice input
		if event.key == pg.K_1:
			#Both players selected so deselect player 1
			if all(item is True for item in self.players):
				self.toggle_player(0, "large", "small")
			# No players selected so select player 1
			elif all(item is False for item in self.players):  
				self.toggle_player(0, "large", "small")
			# Player 1 already selected so deselect player 1
			elif self.players[0]:  
				self.toggle_player(0, "small", "small")
				# Player 2 selected so player 1 selected
			elif self.players[1] and not self.players[0]: 
				self.toggle_player(0, "small", "large")

		if event.key == pg.K_2:
			# Both players selected so deselect player 2
			if all(item is True for item in self.players):
				self.toggle_player(1, "large", "small")
			# No players selected so select player 2
			elif all(item is False for item in self.players): 
				self.toggle_player(1, "large", "small")
			# Player 2 already selected so deselect player 2
			elif self.players[1] and not self.players[0]: 
				self.toggle_player(1, "small", "small")
			# Player 1 selected and player 2 selected
			elif self.players[0] and not self.players[1]: 
				self.toggle_player(1, "small", "large")

		#code to start game after player select
		if event.key == pg.K_RETURN:
			if any(self.players):
				# self.start_mobs.empty() #Check this later
				self.game.change_state("play")

	def check_joystick1(self):
		try:
			#Select player 1
			# Player 1 num 3 button
			if self.game.joystick_handler1.is_button_pressed(2):
				# No players selected so select player 1
				if all(item is False for item in self.game.players):  
					self.toggle_player(0, "large", "small")
				#Player 2 is selected 
				elif self.game.players[1] and not self.players[0]:
					self.toggle_player(0, "small", "large")
			#Deselect player 1
			# Player 1 num 4 button
			if self.game.joystick_handler1.is_button_pressed(3):
				#Both players selected
				if all(item is True for item in self.game.players):
					self.toggle_player(0, "large", "small")	
				#Player 1 selected		
				elif self.game.players[0]:
					self.toggle_player(0, "small", "small")				
	
			#Start game
			# Player 1 start button
			if self.game.joystick_handler1.is_button_pressed(9):
				if any(self.game.players):
					self.game.change_state("play")
			#exit the game
			# Player 1 select button
			if self.game.joystick_handler1.is_button_pressed(8):
				self.game.quit()			
		except AttributeError as e:
			print(f"Joystick error: {e}")

	def check_joystick2(self):
		try:						
			#Select player 2
			# Player 1 num 3 button Select
			if self.game.joystick_handler2.is_button_pressed(2):
				# No players selected so select player 1
				if all(item is False for item in self.game.players):  
					self.toggle_player(1, "large", "small")
			#Deselect player 2				
			# Player 1 num 4 button Deselect
			if self.game.joystick_handler2.is_button_pressed(3):
				#Both players selected
				if all(item is True for item in self.game.players):
					self.toggle_player(1, "large", "small")
				#Player 2 selected
				elif self.game.players[1]:
					self.toggle_player(1, "small", "small")
		
			#Start game
			# Player 2 start button
			if self.game.joystick_handler2.is_button_pressed(9):
				if any(self.game.players):
					self.game.change_state("play")
			#exit the game
			# Player 2 select button
			if self.game.joystick_handler2.is_button_pressed(8):
				self.game.quit()			
		except AttributeError as e:
			print(f"Joystick error: {e}")

	def toggle_player(self, player_index, p1button, p2button):
		"""Toggle the state of a player based on index and pass through the button choice."""
		self.game.players[player_index] = not self.game.players[player_index]
		self._update_button_sizes(p1button, p2button)

	def _update_button_sizes(self, p1button, p2button):
		"""Update button sizes"""
		self.player1_button.button_size = p1button
		self.player2_button.button_size = p2button

	def update(self):
		self.start_mobs.update()

	def draw(self):
		self.game.win.blit(self.background, self.background_rect)
		# draw player images
		if all(item is True for item in self.game.players): #Both players are playing
			self.game.win.blit(self.player1_start_img, (46, 607))
			self.game.win.blit(self.player2_start_img, (506, 607))
		elif self.game.players[0]: #player 1 playing
			self.game.win.blit(self.player1_start_img, (46, 607))
		elif self.game.players[1]: #player 2 playing
			self.game.win.blit(self.player2_start_img, (506, 607))

		self.start_mobs.draw(self.game.win)
		pg.display.update()


class StartQuest(FlashingSprite):
    def __init__(self, game, x, y):
        image = game.resource_manager.get_sprite_image("press_to_start")
        rect = image.get_rect(center=(x, y))
        super().__init__(image, rect)


class StartButtons(pg.sprite.Sprite):
	"""docstring for StartButtons"""
	def __init__(self, game, player_num, x):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image_type = player_num
		self.button_size = "small"
		self.image = f"{self.image_type}up_button_{self.button_size}"
		self.image = self.game.resource_manager.get_sprite_image(self.image)
		self.rect = self.image.get_rect()
		self.x = x
		self.rect.center = (self.x, 710)

	def update(self):
		self.image = self.game.resource_manager.get_sprite_image(f"{self.image_type}up_button_{self.button_size}")
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, 710)

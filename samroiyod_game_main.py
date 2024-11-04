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

import start
import pause
import methods as meth
import constants as const
from game_over import GameOverScreen
from sprites import Player1, Player2, Mob, Boss
from hyperspace import hyperspace
from resource_manager import ResourceManager, load_high_score
from game_checks import CheckEnemy, CheckPlayer, CheckLevel

class Game(object):
	def __init__(self):
		#Initialize game window, etc
		#set game screen placement
		environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (const.COMX,const.COMY)
		pg.mixer.pre_init(44100, -16, 1, 512)
		pg.init()
		# pg.joystick.init()
		self.initialize_joysticks()

		#Set logo and gamescreen etc
		self.win = pg.display.set_mode((const.SCREENWIDTH,const.SCREENHEIGHT))
		try:
			self.logo = pg.image.load(path.join(const.IMAGE_FOLDER, "eplogo_small.png"))
		except pg.error as e:
			print(f"Failed to load logo: {e}")
		pg.display.set_icon(self.logo)
		pg.display.set_caption(f"{const.GAMENAME} {const.__VERSION__}")

		self.clock = pg.time.Clock()
		self.resource_manager = ResourceManager()
		self.load_data()

		#Define game variables
		self.game_on = True
		self.rand_delay = random.randrange(8400,12000)
		self.last_update = pg.time.get_ticks()
		self.boss_last_update = pg.time.get_ticks()
		self.sound_last_update = pg.time.get_ticks()
		self.sound = True
		self.game_level = 1
		self.number_of_players = 0
		self.boss = None #Created first for pause game check
		self.played_high_score_sound = False


	def initialize_joysticks(self):
		#Look for joysticks and initlaize them
		self.joystick_count = pg.joystick.get_count()
		self.joystick_list = []
		for i in range(self.joystick_count):
			self.joystick = pg.joystick.Joystick(i)
			self.joystick.init()
			self.joystick_list.append(self.joystick)

		if self.joystick_count == 2:
			self.joystick1 = self.joystick_list[0]
			self.joystick2 = self.joystick_list[1]
		elif self.joystick_count == 1:
			self.joystick1 = self.joystick_list[0]

	def load_data(self):
		self.resource_manager.load_all_resources()
		#Load all images
		self.sprite_sheet = self.resource_manager.get_image("spritesheet")
		self.background = self.resource_manager.get_image("game_screen")
		self.background_rect = self.background.get_rect()
		#Load all games sounds
		self.high_score_sound = pg.mixer.Sound(self.resource_manager.get_sound("high_score_sound"))
		self.high_score_sound.set_volume(0.6)

		# self.enemy_sounds = []
		# for snd in ['fastinvader1.wav','fastinvader2.wav','fastinvader3.wav','fastinvader4.wav']:
		# 	self.enemy_sounds.append(pg.mixer.Sound(snd))
		# self.enemy_sounds[0].set_volume(0.08)
		# self.enemy_sounds[3].set_volume(0.1)

		#Load high score
		self.high_score = load_high_score()
		self.orig_high_score = self.high_score

	def newmob(self, x, y):
		self.enemy = Mob(x, y, "samroy", 100,  g)
		self.all_sprites.add(self.enemy)
		self.mobs.add(self.enemy)

	# def level_check(self):
	# 	if len(self.mobs) + len(self.Bmobs) <= 0 and not self.expl.alive():
	# 		for bullet in self.player1_bullets.sprites():
	# 			bullet.kill()
	# 		self.player1_bullets.empty()
	# 		for bullet in self.player1_bullets.sprites():
	# 			bullet.kill()
	# 		self.player2_bullets.empty()
	# 		for bullet in self.mob_bullets.sprites():
	# 			bullet.kill()
	# 		self.mob_bullets.empty()
	# 		for powerup in self.powerups.sprites():
	# 			powerup.kill()
	# 		self.powerups.empty()
	# 		if len(self.bosses) > 0:
	# 			self.boss.kill()
	# 			self.boss.sound.fadeout(1500)
	# 		self.game_level += 1
	# 		#Player animation
	# 		#if len(self.player_group) == 2:
	# 		while True:
	# 			self.clock.tick(120)
	# 			if len(self.player_group) == 2:
	# 				self.player1.move_to_center_anim(xpos=round(const.SCREENWIDTH/3))
	# 				self.player2.move_to_center_anim(xpos=round(const.SCREENWIDTH / 3)*2)
	# 				if self.player1.rect.centerx == round(const.SCREENWIDTH/3) and self.player2.rect.centerx == round(const.SCREENWIDTH / 3)*2:
	# 					break
	# 			elif len(self.player_group) == 1:
	# 				for player in self.player_group:
	# 					player.move_to_center_anim(xpos=const.SCREENWIDTH/2)
	# 				if player.rect.centerx == const.SCREENWIDTH/2:
	# 					break
	# 			else:
	# 				break
	# 			self.draw()
	# 		while True:
	# 			if len(self.player_group) > 0:
	# 				self.clock.tick(140)
	# 				for player in self.player_group:
	# 					player.blastoff_anim()
	# 				if player.rect.top == const.SCREENHEIGHT/2:
	# 					break
	# 			else:
	# 				break
	# 			self.draw()
	# 		return True

	def add_boss(self):
		now = pg.time.get_ticks()
		if now - self.boss_last_update >= self.rand_delay:
			self.boss_last_update = now
			self.rand_delay = random.randrange(4600,22000)
			if len(self.bosses) < 1 and self.player1.alive():
				self.boss = Boss(g)
				self.all_sprites.add(self.boss)
				self.bosses.add(self.boss)

		#return(self.p1score)

	def add_mobs(self):
		Bmobs_y_list = [100, 166]
		for ypos in Bmobs_y_list:
			for i in range(10):
				self.bigenemy = Mob(((i+1)*70)-15, ypos, "ep", 50,  g)
				self.all_sprites.add(self.bigenemy)
				self.Bmobs.add(self.bigenemy)
		mob_y_list = [227, 297, 367]
		for ypos in mob_y_list:
			for i in range (10):
				self.newmob(((i+1)*70)-15, ypos)
				
	def new(self):
		#Start a new game
		self.start_screen_pass = False
		self.all_sprites = pg.sprite.Group()
		self.player_group = pg.sprite.Group()
		self.player1_bullets = pg.sprite.Group()
		self.player2_bullets = pg.sprite.Group()
		self.mob_bullets = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.Bmobs = pg.sprite.Group()
		self.bosses = pg.sprite.Group()
		self.powerups = pg.sprite.Group()
		#choose 1 or 2 players
		if self.number_of_players == 2:
			self.p2score=0
			self.player2 = Player2(xpos=(const.SCREENWIDTH / 3)*2, game=g)
			self.player_group.add(self.player2)
			self.all_sprites.add(self.player2)
			self.player1 = Player1(xpos=const.SCREENWIDTH / 3, game=g)
		else:
			self.player1 = Player1(xpos=const.SCREENWIDTH / 2, game=g)
		self.p1score=0
		self.player_group.add(self.player1)
		self.all_sprites.add(self.player1)
		self.add_mobs()
		self.enemy_checks = CheckEnemy(g)
		self.player_checks = CheckPlayer(g)
		self.level_checks = CheckLevel(g)

		# self.waiting = True
		pg.mixer.music.load(self.resource_manager.get_music("game_music"))
		pg.mixer.music.set_volume(0.2)
		pg.mixer.music.play(loops=-1)
		self.run()

	def run(self):
		#Game loop
		self.playing = True
		while self.playing:
			self.clock.tick(const.FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		#Game loop - update
		self.all_sprites.update()

		#Play enemy move sound
		# self.play_mob_movesound()

		#Spawn a boss randomly
		self.add_boss()

		#Check to see if a bullet hit a mob
		if self.number_of_players == 2:
			self.enemy_checks.enemy_hit_check(self.mobs, 10, self.player2_bullets, False)
			self.enemy_checks.enemy_hit_check(self.Bmobs, 30, self.player2_bullets, False)
			self.enemy_checks.enemy_hit_check(self.bosses, 100, self.player2_bullets, True)

		self.enemy_checks.enemy_hit_check(self.mobs, 10, self.player1_bullets, False)
		self.enemy_checks.enemy_hit_check(self.Bmobs, 30, self.player1_bullets, False)
		self.enemy_checks.enemy_hit_check(self.bosses, 100, self.player1_bullets, True)

		#Check if player has killed all the mobs
		if self.level_checks.level_check():
			#reset all mobs
			self.move_delay = 600
			self.enemy_checks.speedx = 5
			self.enemy_checks.mob_direction = True
			self.add_mobs()
			#check what players are alive set at the bottom
			for player in self.player_group:
				player.rect.bottom = const.SCREENHEIGHT - 6

		#Check to see if a mob bullet has hit either player
		if self.number_of_players == 2:
			self.player_checks.player_hit_by_bullet(self.player2)
		self.player_checks.player_hit_by_bullet(self.player1)

		if len(self.player_group) == 0 and not self.player_checks.expl.alive():
			self.playing = False

		#Check to see if a mob has hit either player
		if self.number_of_players == 2:
			self.player_checks.player_hit_by_mob(self.player2)
		self.player_checks.player_hit_by_mob(self.player1)

		#Check if enemies have hit the walls and update movement
		now = pg.time.get_ticks()
		if now - self.last_update >= self.enemy_checks.move_delay:
			self.last_update = now
			# self.enemy_check()
			self.enemy_checks.enemy_direction_check()

		#Update enemy speed
		self.enemy_checks.update_enemy_speed()
		#Check for new high score
		meth.new_high_score_check(g)

	def events(self):
		#Game loop - events
		for event in pg.event.get():#exit loop
			if event.type == pg.QUIT:
				if self.playing:
					self.playing = False
				self.game_on = False
				self.waiting = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					if self.playing:
						self.playing = False
					self.game_on = False
					self.waiting = False
				if event.key == pg.K_p:
					self.pause = pause.Pause(g)
					self.pause.show()
			try:
				if self.joystick1.get_button(8) or self.joystick2.get_button(6): #exit game
					if self.playing:
						self.playing = False
					self.game_on = False
					self.waiting = False
				if self.joystick1.get_button(9) or self.joystick2.get_button(7):
					#pause and unpause
					self.pause()
			except AttributeError:
				pass

	def draw(self):
		#Game loop - draw
		self.win.blit(self.background, self.background_rect)
		if self.number_of_players == 2:
			meth.draw_text(surf=self.win, text=str(self.p2score), size=18, x=557, y=6)
			self.draw_shields(surf=self.win, x=608, y=8, shield_amm=self.player2.shield)
			self.draw_lives(surf=self.win, x=720, y=3, player=self.player2)
		meth.draw_text(surf=self.win, text=str(self.p1score), size=18, x=112, y=6)
		meth.draw_text(surf=self.win, text=str(self.high_score), size=18, x=const.SCREENWIDTH/2, y=4)
		meth.draw_shields(surf=self.win, x=166, y=8, shield_amm=self.player1.shield)
		meth.draw_lives(surf=self.win, x=278, y=3, player=self.player1)
		self.all_sprites.draw(self.win)
		pg.display.update()

print(sys.executable)

if __name__ == '__main__':
	print("Author:", const.__AUTHOR__)
	print("App version:", const.__VERSION__)

	g = Game()
	while g.game_on:
		start_screen = start.StartScreen(g)
		start_screen.show()
		if g.game_on == False:
			break
		g.new()
		game_over_screen = GameOverScreen(g)
		game_over_screen.show()


	pg.quit()
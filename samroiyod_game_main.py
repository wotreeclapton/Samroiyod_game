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
__author__ = 'Mr Steven J Walden'
__version__ = '1.0.1'

from os import environ
import sys
import random
import pygame as pg

import methods as meth
from methods import change_dir
import sprites
from sprites import Player1, Player2, Player1Bullet, Player2Bullet, MobBullet, Mob, Boss, PowerUp, Explosion, StartMob, StartButtons
from hyperspace import hyperspace

class Game(object):
	def __init__(self):
		#Initialize game window, etc
		#set game screen placement
		environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (meth.COMX,meth.COMY)
		pg.mixer.pre_init(44100, -16, 1, 512)
		pg.init()
		pg.joystick.init()

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

		#Set logo and gamescreen etc
		self.win = pg.display.set_mode((meth.SCREENWIDTH,meth.SCREENHEIGHT))
		with change_dir('img'):
			self.logo = pg.image.load('eplogo_small.png')
		pg.display.set_icon(self.logo)
		pg.display.set_caption(f'Samroiyod invaders V {__version__}')
		self.clock = pg.time.Clock()

		self.load_data()

		#Define game variables
		self.rand_delay = random.randrange(8400,12000)
		self.last_update = pg.time.get_ticks()
		self.boss_last_update = pg.time.get_ticks()
		self.sound_last_update = pg.time.get_ticks()
		self.sound = True
		self.mob_direction =True
		self.direction_switch = False
		self.game_on = True
		self.move_delay = 600
		self.speedx = 5
		self.movey = 12
		self.game_level = 1
		self.start_screen_pass = False

	def load_data(self):
		#Load all image graphics
		with change_dir('img'):
			self.sprite_sheet = sprites.Spritesheet("Samroiyodgame_img_sheet.png")
			self.background = pg.image.load('Schoolbg.jpg').convert()
			self.start_background = pg.image.load('start_screen.jpg').convert()
			self.go_background = pg.image.load('game_over_screen.jpg').convert()
		self.background_scaled = pg.transform.scale(self.background, (meth.SCREENWIDTH,meth.SCREENHEIGHT))
		self.start_background_scaled = pg.transform.scale(self.start_background, (meth.SCREENWIDTH,meth.SCREENHEIGHT))
		self.go_background_scaled = pg.transform.scale(self.go_background, (meth.SCREENWIDTH,meth.SCREENHEIGHT))
		self.background_rect = self.background_scaled.get_rect()
		self.player_one_img = self.sprite_sheet.get_image(0, 965, 243, 45)
		self.player_two_img = self.sprite_sheet.get_image(0, 1014, 243, 45)
		self.press_start_img = self.sprite_sheet.get_image(248, 964, 379, 58)
		self.press_start_img_rect = self.press_start_img.get_rect()
		self.paused_img = self.sprite_sheet.get_image(640, 964, 207, 57)
		self.paused_img_rect = self.paused_img.get_rect()

		#Load all games sounds
		with change_dir('snd'):
			self.shoot_sound = pg.mixer.Sound('bullet_shoot.wav')
			self.shoot_sound.set_volume(0.04)
			self.normal_expl_sound = pg.mixer.Sound('enemy_killed.wav')
			self.normal_expl_sound.set_volume(0.04)
			self.high_score_sound = pg.mixer.Sound('new_highscore.ogg')
			self.high_score_sound.set_volume(0.6)
			self.enemy_sounds = []
			for snd in ['fastinvader1.wav','fastinvader2.wav','fastinvader3.wav','fastinvader4.wav']:
				self.enemy_sounds.append(pg.mixer.Sound(snd))
			self.enemy_sounds[0].set_volume(0.08)
			self.enemy_sounds[3].set_volume(0.1)
			self.expl_sounds = []
			for snd in ['Explosion1.wav','Explosion2.wav']:
				self.expl_sounds.append(pg.mixer.Sound(snd))
			self.boss_sound = pg.mixer.Sound('ufo_lowpitch.wav')
			self.boss_sound.set_volume(0.05)
			self.powerup_sounds = []
			for snd in ['guns.wav','shield.wav','extra_life.wav','hyperspace_collect.wav']:
				self.powerup_sounds.append(pg.mixer.Sound(snd))
			self.powerup_sounds[0].set_volume(0.15)
			self.powerup_sounds[1].set_volume(0.18)
			self.powerup_sounds[2].set_volume(0.1)
			self.powerup_sounds[3].set_volume(0.3)
			self.death_explosion = pg.mixer.Sound('death_explosion.wav')
			self.death_explosion.set_volume(0.5)

		#Load high score
		with change_dir('resources'):
			try:
				with open('high_score.bat', 'r') as h_score_file:
					self.high_score = int(h_score_file.read())
					self.orig_high_score = self.high_score
			except FileNotFoundError:
				self.high_score = 0
				self.orig_high_score = self.high_score

	def newmob(self, x, y):
		self.enemy = Mob(x, y, 'mob', 100,  g)
		self.all_sprites.add(self.enemy)
		self.mobs.add(self.enemy)

	def enemy_check(self):
		for enemy in self.mobs.sprites() + self.Bmobs.sprites():
			if enemy.rect.centerx >= meth.SCREENWIDTH - 25 or enemy.rect.centerx <= 25:
				self.direction_switch = True

		if self.direction_switch and self.mob_direction:
			self.direction_switch = False
			self.mob_direction = False
			for mob in self.mobs.sprites() + self.Bmobs.sprites():
				mob.rect.y += self.movey
		elif self.direction_switch and not self.mob_direction:
			self.direction_switch = False
			self.mob_direction = True
			for mob in self.mobs.sprites() + self.Bmobs.sprites():
				mob.rect.y += self.movey

	def level_check(self):
		if len(self.mobs) + len(self.Bmobs) <= 0 and not self.expl.alive():
			for bullet in self.player1_bullets.sprites():
				bullet.kill()
			self.player1_bullets.empty()
			for bullet in self.player1_bullets.sprites():
				bullet.kill()
			self.player2_bullets.empty()
			for bullet in self.mob_bullets.sprites():
				bullet.kill()
			self.mob_bullets.empty()
			for powerup in self.powerups.sprites():
				powerup.kill()
			self.powerups.empty()
			if len(self.bosses) > 0:
				self.boss.kill()
				self.boss_sound.fadeout(1500)
			self.game_level += 1
			#Player animation
			#if len(self.player_group) == 2:
			while True:
				self.clock.tick(120)
				if len(self.player_group) == 2:
					self.player1.move_to_center_anim(xpos=round(meth.SCREENWIDTH/3))
					self.player2.move_to_center_anim(xpos=round(meth.SCREENWIDTH / 3)*2)
					if self.player1.rect.centerx == round(meth.SCREENWIDTH/3) and self.player2.rect.centerx == round(meth.SCREENWIDTH / 3)*2:
						break
				elif len(self.player_group) == 1:
					for player in self.player_group:
						player.move_to_center_anim(xpos=meth.SCREENWIDTH/2)
					if player.rect.centerx == meth.SCREENWIDTH/2:
						break
				else:
					break
				self.draw()
			while True:
				if len(self.player_group) > 0:
					self.clock.tick(140)
					for player in self.player_group:
						player.blastoff_anim()
					if player.rect.top == meth.SCREENHEIGHT/2:
						break
				else:
					break
				self.draw()
			return True

	def add_boss(self):
		now = pg.time.get_ticks()
		if now - self.boss_last_update >= self.rand_delay:
			self.boss_last_update = now
			self.rand_delay = random.randrange(4600,22000)
			if len(self.bosses) < 1 and self.player1.alive():
				self.boss = Boss(g)
				self.all_sprites.add(self.boss)
				self.bosses.add(self.boss)
				self.boss_sound.play(-1)

	def enemy_hit(self, enemy, score_amm, bulletlist, check_group_type):
		hits = pg.sprite.groupcollide(enemy, bulletlist, True, True)
		for hit in hits:
			if bulletlist == self.player2_bullets:
				self.p2score += score_amm
				if self.p2score > self.high_score: #Update high score
					self.high_score = self.p2score
			else:
				self.p1score += score_amm
				if self.p1score > self.high_score: #Update high score
					self.high_score = self.p1score
			if check_group_type: #Bool value for checking the right group
				self.boss_sound.stop()
				random.choice(self.expl_sounds).play()
				if random.random() >= 0.7:
					self.powerup = PowerUp(hit.rect.center, 'boss', g)
					self.all_sprites.add(self.powerup)
					self.powerups.add(self.powerup)
				self.expl = Explosion(hit.rect.center, 'boss', 0, g)
			else:
				self.normal_expl_sound.play()
				if random.random() >= 0.9:
					self.powerup = PowerUp(hit.rect.center, 'norm', g)
					self.all_sprites.add(self.powerup)
					self.powerups.add(self.powerup)
				self.expl = Explosion(hit.rect.center, 'lg', 24, g)
			self.all_sprites.add(self.expl)


		#return(self.p1score)

	def add_mobs(self):
		Bmobs_y_list = [100, 166]
		for ypos in Bmobs_y_list:
			for i in range(10):
				self.bigenemy = Mob(((i+1)*70)-15, ypos, 'Bmob', 50,  g)
				self.all_sprites.add(self.bigenemy)
				self.Bmobs.add(self.bigenemy)
		mob_y_list = [227, 297, 367]
		for ypos in mob_y_list:
			for i in range (10):
				self.newmob(((i+1)*70)-15, ypos)

	def powerup_collect(self, player):
		hits = pg.sprite.spritecollide(player, self.powerups, True)
		for hit in hits:
			if hit.image == self.powerup.powerup_images['norm'][0]: #increase the guns
				self.powerup_sounds[0].play()
				player.powerup()

			if hit.image == self.powerup.powerup_images['norm'][1]: #increase the shields
				self.powerup_sounds[1].play()
				#stop the shield decreasing for a short time and add moving shield
				player.shieldup()
				# if player.shield < 100:
				# 	player.shield += random.randrange(10, 40)
				# 	if player.shield > 100:
				# 		player.shield = 100

			if hit.image == self.powerup.powerup_images['boss'][0]:
				#give an extra life if lives are less than three
				self.powerup_sounds[2].play()
				if player.lives < 3:
					player.lives += 1

			if hit.image == self.powerup.powerup_images['boss'][1]:
				#starts the hyperspace level
				self.powerup_sounds[3].play()
				# self.hyperspace()

	def draw_shields(self, surf, x, y, shield_amm):
		if shield_amm <= 0:
			shield_amm = 0
		self.bar_length = 100
		self.bar_height = 13
		self.fill = (shield_amm / 100) * self.bar_length
		self.outline_rect = pg.Rect(x, y, self.bar_length, self.bar_height)
		self.fill_rect = pg.Rect(x, y, self.fill, self.bar_height)
		pg.draw.rect(surf, meth.GREEN, self.fill_rect)
		pg.draw.rect(surf, meth.WHITE, self.outline_rect, 1)

	def player_death(self, hit, player):
		self.expl = Explosion(hit, 'boss', 100, g)
		self.all_sprites.add(self.expl)
		if len(self.player_group) == 2:
			#check to see if both player are dead
			player.kill()
		else:
			#removes all the bullets after player death
			for bullet in self.mob_bullets.sprites():
				bullet.kill()
			self.mob_bullets.empty()
			self.powerups.empty()
			pg.mixer.music.fadeout(2000)
			self.enemy_sounds[0].stop()
			self.enemy_sounds[3].stop()
			self.death_explosion.play()
			self.boss_sound.fadeout(2000)
			player.kill()
		try:
			if player == self.player2:
				self.moving_shield2.kill()
		except AttributeError:
			pass
		try:
			if player == self.player1:
				self.moving_shield1.kill()
		except AttributeError:
			pass

	def draw_lives(self, surf, x, y, player):
		self.player_image_resized = pg.transform.scale(player.image, (20, 20))
		for i in range (player.lives):
			surf.blit(self.player_image_resized, (x + (i * 25), y))

	def update_enemy_speed(self):
		mob_count = len(self.mobs.sprites()) + len(self.Bmobs.sprites())
		if mob_count <= 4:
			self.move_delay = 30
			self.speedx = 12
			self.movey = 50
		elif mob_count <= 8:
			self.move_delay = 80
			self.movey = 30
		elif mob_count <= 12:
			self.move_delay = 200
			self.speedx = 9
			self.movey =20
		elif mob_count <= 22:
			self.move_delay = 300
			self.speedx = 7
			self.movey =18
		elif mob_count <= 32:
			self.move_delay = 400
			self.speedx = 6
			self.movey =14

	def player_hit(self, player):
		#Check to see if a bullet has hit the player
		hits = pg.sprite.spritecollide(player, self.mob_bullets, True)
		for hit in hits:
			self.expl = Explosion((hit.rect.x, hit.rect.y), 'sm', 25, g)
			self.all_sprites.add(self.expl)
			#activate moving sheild if shield powerup is still active
			if player.active_shield == True:
				try:
					if player == self.player2:
						self.moving_shield2 = sprites.Shield2(xpos=player.rect.centerx, game=g)
						self.all_sprites.add(self.moving_shield2)
				except AttributeError:
					pass
				try:
					if player == self.player1:
						self.moving_shield1 = sprites.Shield1(xpos=player.rect.centerx, game=g)
						self.all_sprites.add(self.moving_shield1)
				except AttributeError:
					pass
			else:
				player.shield -= random.randrange(10,30)
			if player.shield <= 0:
				player.lives -= 1
				#move the player off the screen
				player.hide()

				if player.lives <= 0:
					self.player_death(hit=hit.rect.center, player=player)
				player.shield = 100

	def player_hit_by_mob(self, player):
		#Check to see if a mob has hit the player
		hits = pg.sprite.spritecollide(player, self.mobs, True) + pg.sprite.spritecollide(player, self.Bmobs, True)
		for hit in hits:
			self.player_death(hit=hit.rect.center, player=player)
			player.shield = 0
			player.lives = 0
			player.hide()
			if not self.expl.alive():
				self.playing = False

	def pause(self):
		count = 0
		pause = True
		while pause:
			self.win.blit(self.background_scaled, self.background_rect)
			#display pause writing
			if count <= 300:
				self.win.blit(self.paused_img, (meth.SCREENWIDTH / 2 - self.paused_img_rect.width / 2, meth.SCREENHEIGHT / 2))
				#self.draw_text(surf=self.win, text="Paused", size=68, x=400, y=meth.SCREENHEIGHT / 2, pos=1)
			if count >= 600:
				count = 0
			count += 1
			pg.display.update()
			#unpause
			for event in pg.event.get():
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_p:
						pause = False
				try:
					if self.joystick.get_button(9):
						pause = False
				except AttributeError:
					pass

	def new(self):
		#Start a new game
		self.start_screen_pass = False
		self.play_high_score_sound = True
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
			self.player2 = Player2(xpos=(meth.SCREENWIDTH / 3)*2, game=g)
			self.player_group.add(self.player2)
			self.all_sprites.add(self.player2)
			self.player1 = Player1(xpos=meth.SCREENWIDTH / 3, game=g)
		else:
			self.player1 = Player1(xpos=meth.SCREENWIDTH / 2, game=g)
		self.p1score=0
		self.player_group.add(self.player1)
		self.all_sprites.add(self.player1)
		self.add_mobs()

		self.waiting = True
		with change_dir('snd'):
			pg.mixer.music.load('tgfcoder-FrozenJam-SeamlessLoop.ogg')
		pg.mixer.music.set_volume(0.2)
		pg.mixer.music.play(loops=-1)
		self.run()

	def run(self):
		#Game loop
		self.playing = True
		while self.playing:
			self.clock.tick(meth.FPS)
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
			self.enemy_hit(enemy=self.mobs, score_amm=10, bulletlist=self.player2_bullets, check_group_type=False)
			self.enemy_hit(enemy=self.Bmobs, score_amm=30, bulletlist=self.player2_bullets, check_group_type=False)
			self.enemy_hit(enemy=self.bosses, score_amm=100, bulletlist=self.player2_bullets, check_group_type=True)

		self.enemy_hit(enemy=self.mobs, score_amm=10, bulletlist=self.player1_bullets, check_group_type=False)
		self.enemy_hit(enemy=self.Bmobs, score_amm=30, bulletlist=self.player1_bullets, check_group_type=False)
		self.enemy_hit(enemy=self.bosses, score_amm=100, bulletlist=self.player1_bullets, check_group_type=True)

		#Check if player has killed all the mobs
		if self.level_check():
			#reset all mobs
			self.move_delay = 600
			self.speedx = 5
			self.mob_direction = True
			self.add_mobs()
			#check what players are alive set at the bottom
			for player in self.player_group:
				player.rect.bottom = meth.SCREENHEIGHT - 6

		#Check to see if a mob bullet has hit either player
		if self.number_of_players == 2:
			self.player_hit(player=self.player2)
		self.player_hit(player=self.player1)

		if len(self.player_group) == 0 and not self.expl.alive():
			self.playing = False

		#Check to see if a mob has hit either player
		if self.number_of_players == 2:
			self.player_hit_by_mob(self.player2)
		self.player_hit_by_mob(self.player1)

		#Check to see if the player has hit a powerup
		if self.number_of_players == 2:
			self.powerup_collect(self.player2)
		self.powerup_collect(self.player1)

		#Check if enemies have hit the walls and update movement
		now = pg.time.get_ticks()
		if now - self.last_update >= self.move_delay:
			self.last_update = now
			self.enemy_check()

		#Update enemy speed
		self.update_enemy_speed()

		#play high score sound
		if self.number_of_players == 2:
			if self.play_high_score_sound == True and self.p2score > self.orig_high_score:
				self.high_score_sound.play()
				self.play_high_score_sound = False
		if self.play_high_score_sound == True and self.p1score > self.orig_high_score:
			self.high_score_sound.play()
			self.play_high_score_sound = False

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
					self.pause()
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
		self.win.blit(self.background_scaled, self.background_rect)
		if self.number_of_players == 2:
			meth.draw_text(surf=self.win, text=str(self.p2score), size=22, x=557, y=2, pos=0)
			self.draw_shields(surf=self.win, x=608, y=8, shield_amm=self.player2.shield)
			self.draw_lives(surf=self.win, x=720, y=3, player=self.player2)
		meth.draw_text(surf=self.win, text=str(self.p1score), size=22, x=112, y=2, pos=0)
		meth.draw_text(surf=self.win, text=str(self.high_score), size=18, x=meth.SCREENWIDTH/2, y=4, pos=1)
		self.draw_shields(surf=self.win, x=166, y=8, shield_amm=self.player1.shield)
		self.draw_lives(surf=self.win, x=278, y=3, player=self.player1)
		self.all_sprites.draw(self.win)
		pg.display.update()

	def show_start_screen(self):
		if self.start_screen_pass:
			pass
		else:
			self.number_of_players = 0
			self.p1 = False
			self.p2 = False
			with change_dir('snd'): #set music
				pg.mixer.music.load('through space.ogg')
			pg.mixer.music.set_volume(1.0)
			pg.mixer.music.play(loops=-1)
			#Add mobs to show
			self.start_mobs = pg.sprite.Group()
			self.start_enemy = StartMob(187, 471, 'mob', 100,  g)
			self.start_benemy = StartMob(319, 471, 'Bmob', 50,  g)
			#add button sprites
			self.player_buttons = StartButtons(game=g)
			#self.player_two_button = StartButtons(button_type=2, button_center=(489, 710), game=g)
			#add to group
			self.start_mobs.add(self.start_enemy)
			self.start_mobs.add(self.start_benemy)
			self.start_mobs.add(self.player_buttons)
			#self.start_mobs.add(self.player_two_button)
			#Game start screen
			s = True
			while s:
				#start loop - events
				for event in pg.event.get():#exit loop
					if event.type == pg.QUIT:
							self.game_on = False
							s = False
					elif event.type == pg.KEYDOWN:
						if event.key == pg.K_1:
							if self.number_of_players == 1:
								self.number_of_players = 0
								self.p1 = False
							elif self.number_of_players == 2:
								self.p1 = True
							elif self.number_of_players == 2 and self.p1 == True:
								self.p1 = False
							else:
								self.number_of_players = 1
								self.count = 0
								self.p1 = True
						if event.key == pg.K_2 and self.player_buttons.image == self.player_buttons.buttons[1]:
							if self.number_of_players == 2:
								self.number_of_players = 1
								self.p2 = False
							else:
								self.number_of_players = 2
								self.p2 = True
								self.count = 0
						if event.key == pg.K_RETURN:
							if self.player_buttons.image == self.player_buttons.buttons[1] and self.p1 == True and self.p2 == True or self.player_buttons.image == self.player_buttons.buttons[0] and self.p1 == True:
								s = False
								self.start_mobs.empty()
					try:
						if self.joystick1.get_button(9): #Player 1 start button
							if self.number_of_players == 1:
								self.number_of_players = 0
								self.p1 = False
							elif self.number_of_players == 2:
								self.p1 = True
							elif self.number_of_players == 2 and self.p1 == True:
								self.p1 = False
							else:
								self.number_of_players = 1
								self.count = 0
								self.p1 = True
						if self.joystick2.get_button(7) and self.player_buttons.image == self.player_buttons.buttons[1]: #Player 2 start button
							if self.number_of_players == 2:
								self.number_of_players = 1
								self.p2 = False
							else:
								self.number_of_players = 2
								self.p2 = True
								self.count = 0
						if self.joystick1.get_button(2) or self.joystick2.get_button(0):
							if self.player_buttons.image == self.player_buttons.buttons[1] and self.p1 == True and self.p2 == True or self.player_buttons.image == self.player_buttons.buttons[0] and self.p1 == True:
								s = False
								self.start_mobs.empty()
					except AttributeError:
						pass
				self.start_mobs.update()
				self.win.blit(self.start_background_scaled, self.background_rect)
				#draw player images
				if self.number_of_players == 2 and self.p1 == True:
					self.win.blit(self.player_one_img, (46, 607))
					self.win.blit(self.player_two_img, (506, 607))
				if self.number_of_players == 2 and self.p1 !=True:
					self.win.blit(self.player_two_img, (506, 607))
				if self.number_of_players == 1 and self.p1 == True:
					self.win.blit(self.player_one_img, (46, 607))
				if self.number_of_players != 0: #draw press start text
					if self.count <= 200:
						self.win.blit(self.press_start_img, (meth.SCREENWIDTH / 2 - self.press_start_img_rect.width / 2, 330))
					if self.count >= 400:
						self.count = 0
					self.count += 1

				self.start_mobs.draw(self.win)
				pg.display.update()

	def show_go_screen(self):
		#save high score
		meth.write_high_score(str(self.high_score))
		#Game over/continue screen
		self.win.blit(self.go_background_scaled, self.background_rect)
		#Draw score
		if self.number_of_players == 2:
			meth.draw_text(surf=self.win, text=f"Player 2: {self.p2score}", size=38, x=400, y=535, pos=1)
		meth.draw_text(surf=self.win, text=f"Player 1: {self.p1score}", size=38, x=400, y=471, pos=1)
		pg.mixer.music.fadeout(2000)
		while self.waiting:
			self.clock.tick(meth.FPS)

			for event in pg.event.get():#exit loop
				if event.type == pg.QUIT:
					self.waiting = False
					self.game_on = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE: #Return to start screen
						self.waiting = False
				if event.type == pg.KEYUP:
					if event.key == pg.K_y: #Continue
						self.waiting = False
						self.start_screen_pass = True
				try:
					for joystick in self.joystick_list:
						if self.joystick.get_button(8) or self.joystick.get_button(6): #Select button to return to start screen
							self.waiting = False
						if self.joystick.get_button(9) or self.joystick.get_button(7): #Play button to continue
							self.waiting = False
							self.start_screen_pass = True
				except AttributeError:
					pass

			pg.display.update()

print(sys.executable)

if __name__ == '__main__':
	print("Author:", __author__)
	print("App version:", __version__)

	g = Game()
	while g.game_on:
		g.show_start_screen()
		if g.game_on == False:
			break
		g.new()
		g.show_go_screen()


	pg.quit()






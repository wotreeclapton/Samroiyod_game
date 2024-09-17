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
from methods import change_dir
import sprites
from sprites import Player1, Player2, Player1Bullet, Player2Bullet, MobBullet, Mob, Boss, PowerUp, Explosion, StartMob
from hyperspace import hyperspace
from resource_manager import ResourceManager

class Game(object):
	def __init__(self):
		#Initialize game window, etc
		#set game screen placement
		environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (const.COMX,const.COMY)
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
		self.mob_direction =True
		self.direction_switch = False
		self.move_delay = 600
		self.speedx = 5
		self.movey = 12
		self.game_level = 1
		self.number_of_players = 0

	def load_data(self):
		self.resource_manager.load_all_resources()
		#Load all image graphics

		self.sprite_sheet = self.resource_manager.get_image("spritesheet")
		self.background = self.resource_manager.get_image("game_screen")
		self.background_rect = self.background.get_rect()
		
		# self.paused_img = self.resource_manager.load_spritesheet_image("spritesheet", 640, 964, 207, 57)
		# self.paused_img_rect = self.paused_img.get_rect()

		#Load all games sounds
		self.high_score_sound = pg.mixer.Sound(self.resource_manager.get_sound("high_score_sound"))
		self.high_score_sound.set_volume(0.6)

		# self.enemy_sounds = []
		# for snd in ['fastinvader1.wav','fastinvader2.wav','fastinvader3.wav','fastinvader4.wav']:
		# 	self.enemy_sounds.append(pg.mixer.Sound(snd))
		# self.enemy_sounds[0].set_volume(0.08)
		# self.enemy_sounds[3].set_volume(0.1)

		#Load high score
		try:
			with open(path.join(const.RESOURCES_FOLDER, "high_score.bat"), "r") as h_score_file:
				self.high_score = int(h_score_file.read())
				self.orig_high_score = self.high_score
		except FileNotFoundError:
			self.high_score = 0
			self.orig_high_score = self.high_score

	def newmob(self, x, y):
		self.enemy = Mob(x, y, "samroy", 100,  g)
		self.all_sprites.add(self.enemy)
		self.mobs.add(self.enemy)

	def enemy_check(self):
		for enemy in self.mobs.sprites() + self.Bmobs.sprites():
			if enemy.rect.centerx >= const.SCREENWIDTH - 25 or enemy.rect.centerx <= 25:
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
				self.boss.sound.fadeout(1500)
			self.game_level += 1
			#Player animation
			#if len(self.player_group) == 2:
			while True:
				self.clock.tick(120)
				if len(self.player_group) == 2:
					self.player1.move_to_center_anim(xpos=round(const.SCREENWIDTH/3))
					self.player2.move_to_center_anim(xpos=round(const.SCREENWIDTH / 3)*2)
					if self.player1.rect.centerx == round(const.SCREENWIDTH/3) and self.player2.rect.centerx == round(const.SCREENWIDTH / 3)*2:
						break
				elif len(self.player_group) == 1:
					for player in self.player_group:
						player.move_to_center_anim(xpos=const.SCREENWIDTH/2)
					if player.rect.centerx == const.SCREENWIDTH/2:
						break
				else:
					break
				self.draw()
			while True:
				if len(self.player_group) > 0:
					self.clock.tick(140)
					for player in self.player_group:
						player.blastoff_anim()
					if player.rect.top == const.SCREENHEIGHT/2:
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
				self.boss.sound.stop()
				if random.random() >= 0.7:
					self.powerup = PowerUp(hit.rect.center, 'boss', g)
					self.all_sprites.add(self.powerup)
					self.powerups.add(self.powerup)
				self.expl = Explosion(hit.rect.center, 'boss', 0, g, "boss")
			else:
				if random.random() >= 0.9:
					self.powerup = PowerUp(hit.rect.center, 'norm', g)
					self.all_sprites.add(self.powerup)
					self.powerups.add(self.powerup)
				self.expl = Explosion(hit.rect.center, 'lg', 24, g, "mob")
			self.all_sprites.add(self.expl)


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
				
	"""Put this section into the poweup sprite update"""
	def powerup_collect(self, player):
		hits = pg.sprite.spritecollide(player, self.powerups, True)
		for hit in hits:
			if hit.image == self.resource_manager.get_sprite_image("powerup_norm1"): #increase the guns
				self.resource_manager.get_sound("powerup_gun_sound").play()
				player.powerup()

			if hit.image == self.resource_manager.get_sprite_image("powerup_norm2"):  # increase the shields
				self.resource_manager.get_sound("powerup_shield_sound").play()
				#stop the shield decreasing for a short time and add moving shield
				player.shieldup()
				# if player.shield < 100:
				# 	player.shield += random.randrange(10, 40)
				# 	if player.shield > 100:
				# 		player.shield = 100

			if hit.image == self.resource_manager.get_sprite_image("powerup_boss1"):
				#give an extra life if lives are less than three
				self.resource_manager.get_sound("powerup_life_sound").play()
				if player.lives < 3:
					player.lives += 1

			if hit.image == self.resource_manager.get_sprite_image("powerup_boss2"):
				#starts the hyperspace level
				self.resource_manager.get_sound("powerup_hyperspace_sound").play()
				# self.hyperspace()

	def draw_shields(self, surf, x, y, shield_amm):
		if shield_amm <= 0:
			shield_amm = 0
		self.bar_length = 100
		self.bar_height = 13
		self.fill = (shield_amm / 100) * self.bar_length
		self.outline_rect = pg.Rect(x, y, self.bar_length, self.bar_height)
		self.fill_rect = pg.Rect(x, y, self.fill, self.bar_height)
		pg.draw.rect(surf, const.GREEN, self.fill_rect)
		pg.draw.rect(surf, const.WHITE, self.outline_rect, 1)

	def player_death(self, hit, player):
		if len(self.player_group) == 2:
			self.expl = Explosion(hit, "boss", 100, g, "boss")
			self.all_sprites.add(self.expl)
			#check to see if both player are dead
			player.kill()
		else:
			self.expl = Explosion(hit, "boss", 100, g, "death")
			self.all_sprites.add(self.expl)
			#removes all the bullets after player death
			for bullet in self.mob_bullets.sprites():
				bullet.kill()
			self.mob_bullets.empty()
			self.powerups.empty()
			pg.mixer.music.fadeout(2000)
			# self.enemy_sounds[0].stop()
			# self.enemy_sounds[3].stop()
			self.boss.sound.fadeout(2000)
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
			self.expl = Explosion((hit.rect.x, hit.rect.y), 'sm', 25, g, "boss")
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

	# def pause(self):
	# 	count = 0
	# 	pause = True
	# 	while pause:
	# 		self.win.blit(self.background_scaled, self.background_rect)
	# 		#display pause writing
	# 		if count <= 300:
	# 			self.win.blit(self.paused_img, (const.SCREENWIDTH / 2 - self.paused_img_rect.width / 2, const.SCREENHEIGHT / 2))
	# 			#self.draw_text(surf=self.win, text="Paused", size=68, x=400, y=const.SCREENHEIGHT / 2, pos=1)
	# 		if count >= 600:
	# 			count = 0
	# 		count += 1
	# 		pg.display.update()
	# 		#unpause
	# 		for event in pg.event.get():
	# 			if event.type == pg.KEYDOWN:
	# 				if event.key == pg.K_p:
	# 					pause = False
	# 			try:
	# 				if self.joystick.get_button(9):
	# 					pause = False
	# 			except AttributeError:
	# 				pass

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
				player.rect.bottom = const.SCREENHEIGHT - 6

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
			meth.draw_text(surf=self.win, text=str(self.p2score), size=22, x=557, y=2, pos=0)
			self.draw_shields(surf=self.win, x=608, y=8, shield_amm=self.player2.shield)
			self.draw_lives(surf=self.win, x=720, y=3, player=self.player2)
		meth.draw_text(surf=self.win, text=str(self.p1score), size=22, x=112, y=2, pos=0)
		meth.draw_text(surf=self.win, text=str(self.high_score), size=18, x=const.SCREENWIDTH/2, y=4, pos=1)
		self.draw_shields(surf=self.win, x=166, y=8, shield_amm=self.player1.shield)
		self.draw_lives(surf=self.win, x=278, y=3, player=self.player1)
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






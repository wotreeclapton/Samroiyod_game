#! python 3
'''
SAMROIYOD GAME LAUNCHER developed by Mr Steven J walden
    Nov. 2020
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND
[See License.txt file]
'''
'''
enemy move down check
level up clear bullets and bosses
Joystick prob
powerup rewards
	double points
make bonus level
start screen
game over screen
level bosses
create a delay and message on level change
increase drop speed with less enemys
hyperspace
'''
__author__ = 'Mr Steven J Walden'
__version__ = '1.0.0'

from os import environ
import sys
import random
import pygame as pg

import methods
from methods import change_dir
import sprites
from sprites import Player, Bullet, MobBullet, Mob, Boss, PowerUp, Explosion

class Game(object):
	def __init__(self):
		#Initialize game window, etc		
		#set game screen placement
		environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (methods.COMX,methods.COMY)
		pg.mixer.pre_init(44100, -16, 1, 512)
		pg.init()
		pg.joystick.init()
		
		#Look for joysticks and initlaize them	
		self.joystick_count = pg.joystick.get_count()
		for i in range(self.joystick_count):
			self.joystick = pg.joystick.Joystick(i)
			self.joystick.init()

		#Set logo and gamescreen etc	
		self.win = pg.display.set_mode((methods.SCREENWIDTH,methods.SCREENHEIGHT))
		with change_dir('img'):
			self.logo = pg.image.load('eplogo_small.png')
		pg.display.set_icon(self.logo)
		pg.display.set_caption('Samroiyod invaders V {}'.format(__version__))
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

	def load_data(self):
		#Load all image graphics
		with change_dir('img'):
			self.sprite_sheet = sprites.Spritesheet("Samroiyodgame_img_sheet.png")
			self.background = pg.image.load('Schoolbg.jpg').convert()
		self.background_scaled = pg.transform.scale(self.background, (methods.SCREENWIDTH,methods.SCREENHEIGHT))
		self.background_rect = self.background_scaled.get_rect()


		#Load all games sounds
		with change_dir('snd'):
			self.shoot_sound = pg.mixer.Sound('bullet_shoot.wav')
			self.shoot_sound.set_volume(0.04)
			self.normal_expl_sound = pg.mixer.Sound('enemy_killed.wav')
			self.normal_expl_sound.set_volume(0.04)
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
			for snd in ['guns.wav','shield.wav','extra_life.wav']:
				self.powerup_sounds.append(pg.mixer.Sound(snd))
			self.powerup_sounds[0].set_volume(0.15)
			self.powerup_sounds[1].set_volume(0.16) 
			self.powerup_sounds[2].set_volume(0.1)
			pg.mixer.music.load('tgfcoder-FrozenJam-SeamlessLoop.ogg')
			pg.mixer.music.set_volume(0.2)
			self.death_explosion = pg.mixer.Sound('death_explosion.wav')

	def newmob(self, x, y):
		self.enemy = Mob(x, y, 'mob', 100,  g)
		self.all_sprites.add(self.enemy)
		self.mobs.add(self.enemy)

	def enemy_check(self):
		for enemy in self.mobs.sprites() + self.Bmobs.sprites():
			if enemy.rect.right >= methods.SCREENWIDTH or enemy.rect.left <= 0:
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
			self.bullets.empty()
			self.mob_bullets.empty()
			self.boss.kill()
			self.boss_sound.fadeout(1500)
			self.game_level += 1
			#Player animation
			self.player.player_level_up_anim()
			return True		

	# def play_mob_movesound(self):
	# 	if len(self.mobs) + len(self.Bmobs) > 0 and self.player.alive():
	# 		sound_delay = self.move_delay
	# 		if sound_delay < 150:
	# 			sound_delay = 150
	# 		now = pg.time.get_ticks()
	# 		if now - self.sound_last_update >= sound_delay:
	# 			self.sound_last_update = now
	# 			if self.sound:
	# 				self.enemy_sounds[3].play()
	# 				self.sound = False	
	# 			else:
	# 				self.enemy_sounds[0].play()	
	# 				self.sound = True				

	def add_boss(self):
		now = pg.time.get_ticks()
		if now - self.boss_last_update >= self.rand_delay:
			self.boss_last_update = now
			self.rand_delay = random.randrange(4600,22000)
			if len(self.bosses) < 1 and self.player.alive():
				self.boss = Boss(g)
				self.all_sprites.add(self.boss)
				self.bosses.add(self.boss)
				self.boss_sound.play(-1)	 

	def enemy_hit(self, enemy, score_amm, check_group_type):
		hits = pg.sprite.groupcollide(enemy, self.bullets, True, True)
		for hit in hits:
			self.score += score_amm
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

		return(self.score)
	
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

	def powerup_collect(self):
		hits = pg.sprite.spritecollide(self.player, self.powerups, True)
		for hit in hits:
			if hit.image == self.powerup.powerup_images['norm'][0]: #increase the guns	
				self.powerup_sounds[0].play()
				self.player.powerup()

			if hit.image == self.powerup.powerup_images['norm'][1]: #increase the shields
				self.powerup_sounds[1].play()
				if self.player.shield < 100:
					self.player.shield += random.randrange(10, 40)
					if self.player.shield > 100:
						self.player.shield = 100

			if hit.image == self.powerup.powerup_images['boss'][0]:
				#give an extra life if lives are less than three
				self.powerup_sounds[2].play()
				if self.player.lives < 3:
					self.player.lives += 1

			if hit.image == self.powerup.powerup_images['boss'][1]:
				#starts the bonus level
				pass	

	def draw_text(self, surf, text, size, x, y):
		with change_dir('img'):
			font = pg.font.Font('HARLOWSI.ttf', size)
		self.text_surface = font.render(text, True, methods.WHITE)
		self.text_rect = self.text_surface.get_rect()
		surf.blit(self.text_surface, (x,y))

	def draw_shields(self, surf, x, y, shield_amm):
		if shield_amm <= 0:
			shield_amm = 0
		self.bar_length = 100
		self.bar_height = 13
		self.fill = (shield_amm / 100) * self.bar_length
		self.outline_rect = pg.Rect(x, y, self.bar_length, self.bar_height)
		self.fill_rect = pg.Rect(x, y, self.fill, self.bar_height)
		pg.draw.rect(surf, methods.GREEN, self.fill_rect)
		pg.draw.rect(surf, methods.WHITE, self.outline_rect, 1)

	def player_death(self, hit):
		self.expl = Explosion(hit, 'boss', 170, g)
		self.all_sprites.add(self.expl)
		#removes all the bullets after player death
		for bullet in self.mob_bullets.sprites():
			bullet.kill()
		pg.mixer.music.fadeout(2000)
		self.enemy_sounds[0].stop()
		self.enemy_sounds[3].stop()
		self.death_explosion.play()
		self.boss_sound.fadeout(2000)
		self.player.kill()

	def draw_lives(self, surf, x, y, remaining_lives):
		self.player_image_resized = pg.transform.scale(self.player.image, (20, 20))
		for i in range (self.player.lives):
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

	def new(self):
		#Start a new game
		self.score=0
		self.all_sprites = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		self.mob_bullets = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.Bmobs = pg.sprite.Group()
		self.bosses = pg.sprite.Group()
		self.powerups = pg.sprite.Group()
		self.player = Player(g)
		self.all_sprites.add(self.player)

		self.add_mobs()
		
		self.waiting = True
		pg.mixer.music.play(loops=-1)
		self.run()

	def run(self):
		#Game loop	
		self.playing = True
		while self.playing:
			self.clock.tick(methods.FPS)
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
		self.score = self.enemy_hit(self.mobs, 10, False)	
		self.score = self.enemy_hit(self.Bmobs, 30, False)
		self.score = self.enemy_hit(self.bosses, 100, True)

		#Check if player has killed all the mobs
		if self.level_check():
			#reset all mobs
			self.move_delay = 600
			self.speedx = 5
			self.mob_direction = True
			self.add_mobs()
			self.player.rect.bottom = methods.SCREENHEIGHT - 6

		#Check to see if a bullet has hit the player
		hits = pg.sprite.spritecollide(self.player, self.mob_bullets, True)
		for hit in hits:
			self.player.shield -= random.randrange(10,30)
			self.expl = Explosion((hit.rect.x, hit.rect.y), 'sm', 25, g)
			self.all_sprites.add(self.expl)

			if self.player.shield <= 0:
				self.player.lives -= 1
				#move the player off the screen
				self.player.hide()
				
				if self.player.lives <= 0:
					self.player_death(hit.rect.center)
				self.player.shield = 100

		if not self.player.alive() and not self.expl.alive():			
			self.playing = False

		#Check to see if a mob has hit the player
		hits = pg.sprite.spritecollide(self.player, self.mobs, True) + pg.sprite.spritecollide(self.player, self.Bmobs, True)
		for hit in hits:
			self.player_death(hit.rect.center)
			self.player.shield = 0
			self.player.lives = 0
			self.player.hide()
			if not self.expl.alive():
				self.playing = False
			
		#Check to see if the player has hit a powerup
		self.powerup_collect()

		#Check if enemies have hit the walls and update movement
		now = pg.time.get_ticks()
		if now - self.last_update >= self.move_delay:
			self.last_update = now
			self.enemy_check()			

		#Update enemy speed
		self.update_enemy_speed()

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

	def draw(self):
		#Game loop - draw
		self.win.blit(self.background_scaled, self.background_rect)	
		self.draw_text(self.win, str(self.score), 22, 112, 2)
		self.draw_shields(self.win, 166, 8, self.player.shield)
		self.draw_lives(self.win, 278, 3, self.player.lives)
		self.all_sprites.draw(self.win)
		pg.display.update()

	def show_start_screen(self):
		#Game start screen
		pass

	def show_go_screen(self):
		#Game over/continue screen
		self.win.blit(self.background_scaled, self.background_rect)
		self.draw_text(self.win, "Samroiyod game", 64, methods.SCREENWIDTH / 3, methods.SCREENHEIGHT / 4)
		self.draw_text(self.win, 'Arrow keys to move, Space to fire', 22, methods.SCREENWIDTH /3, methods.SCREENHEIGHT / 2)
		self.draw_text(self.win, 'Press Y to start', 18, methods.SCREENWIDTH / 3, methods.SCREENHEIGHT * 3/4)
		pg.mixer.music.fadeout(2000)
		while self.waiting:
			self.clock.tick(FPS)

			for event in pg.event.get():#exit loop
				if event.type == pg.QUIT:
					self.waiting = False
					g.game_on = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.waiting = False
						g.game_on = False
				if event.type == pg.KEYUP:
					if event.key == pg.K_y:
						self.waiting = False

			pg.display.update()

print(sys.executable)

if __name__ == '__main__':
	print("Author:", __author__)
	print("App version:",__version__)

	g = Game()
	g.show_start_screen()
	while g.game_on:
		g.new()
		g.show_go_screen()


	pg.quit()






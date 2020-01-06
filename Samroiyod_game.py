'''
Inheriting update methods
Explosions for player and boss
lives
powerup rewards
	extra lives
game over screen
Levels
hyperspace
'''
from os import path ,environ
import pygame as pg
import random
from settings import *

#set game screen placement
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (COMX,COMY)
#Initialize everything
pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
pg.joystick.init()


#Look for joysticks and initlaize them	
joystick_count = pg.joystick.get_count()
for i in range(joystick_count):
	joystick = pg.joystick.Joystick(i)
	joystick.init()


#Set logo and gamescreen etc
logo = pg.image.load(path.join(img_folder, 'eplogo_small.png'))
win = pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pg.display.set_icon(logo)
pg.display.set_caption(GAMENAME)
clock = pg.time.Clock()


#Define variables
move_delay = 550
rand_delay = random.randrange(8400,12000)
last_update = pg.time.get_ticks()
boss_last_update = pg.time.get_ticks()

#Set fomts
font_name = pg.font.match_font('arial bold')

#Load all image graphics
background = pg.image.load(path.join(img_folder, 'Schoolbg1.jpg')).convert()
background_scaled = pg.transform.scale(background, (SCREENWIDTH,SCREENHEIGHT))
background_rect = background_scaled.get_rect()
player_image = pg.image.load(path.join(img_folder, 'player1.png')).convert_alpha()
bullet_image = pg.image.load(path.join(img_folder, 'Bullet.png')).convert_alpha()
mob_bullet_image = pg.image.load(path.join(img_folder, 'mob_lazer.png')).convert_alpha()
mob_images = []
bigenemy_images = []
for i in range(20):
	bigenemy_images.append(pg.image.load(path.join(img_folder, 'eplogo' + str(i + 1) + '.png')).convert_alpha())
	mob_images.append(pg.image.load(path.join(img_folder, 'logo' + str(i + 1) + '.png')).convert_alpha())
boss_img = pg.image.load(path.join(img_folder, 'boss_img1.png')).convert_alpha()
powerup_images = []
for img in ['bolt_gold.png','shield_green.png', 'star_bronze.png']:
	powerup_images.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
explosion_anim = []
for i in range(15):
	explosion_anim.append(pg.image.load(path.join(img_folder, 'Explosion' + str(i + 1) + '.png')).convert_alpha())


#Load all games sounds
shoot_sound = pg.mixer.Sound(path.join(sound_folder, 'bullet_shoot.wav'))
shoot_sound.set_volume(0.04)
normal_expl_sound = pg.mixer.Sound(path.join(sound_folder, 'enemy_killed.wav'))
normal_expl_sound.set_volume(0.04)
enemy_sounds = []
for snd in ['fastinvader1.wav','fastinvader2.wav','fastinvader3.wav','fastinvader4.wav']:
	enemy_sounds.append(pg.mixer.Sound(path.join(sound_folder, snd)))
enemy_sounds[0].set_volume(0.02)
enemy_sounds[3].set_volume(0.04)
expl_sounds = []
for snd in ['Explosion1.wav','Explosion2.wav']:
	expl_sounds.append(pg.mixer.Sound(path.join(sound_folder, snd)))
boss_sound = pg.mixer.Sound(path.join(sound_folder, 'ufo_lowpitch.wav'))
boss_sound.set_volume(0.04)
pg.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pg.mixer.music.set_volume(0.2)


#Functions
def newmob(x, y, move_delay):
	enemy = Mob(x, y, move_delay)
	all_sprites.add(enemy)
	mobs.add(enemy)

def enemy_check(mob_group):
	for enemy in mob_group:
		if enemy.rect.right >= SCREENWIDTH:
			for e in mobs:
				e.direction = False
				e.rect.y += 8
			for e in Bmobs:
				e.direction = False
				e.rect.y += 8				
		elif enemy.rect.left <= 0:
			for e in mobs:
				e.direction = True
				e.rect.y += 8
			for e in Bmobs:
				e.direction = True
				e.rect.y += 8

def add_boss():
	if len(bosses) < 1:
		boss = Boss()
		all_sprites.add(boss)
		bosses.add(boss)
		boss_sound.play(-1)	 

def enemy_hit(enemy, score_amm, score, check_group_type):
	hits = pg.sprite.groupcollide(enemy, bullets, True, True)
	for hit in hits:
		score += score_amm
		if check_group_type: #Bool value for checking the right group
			boss_sound.stop()
			random.choice(expl_sounds).play()
			if random.random() >= 0.7:
				powerup = LifePowerUp(hit.rect.center)			
				all_sprites.add(powerup)
				powerups.add(powerup)
		else:
			normal_expl_sound.play()
			if random.random() >= 0.9:
				powerup = PowerUp(hit.rect.center)
				all_sprites.add(powerup)
				powerups.add(powerup)		

		expl = Explosion(hit.rect.center)
		all_sprites.add(expl)		

	return(score)	

def draw_text(surf, text, size, x, y):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	surf.blit(text_surface, (x,y))

def draw_shields(surf, x, y, shield_amm):
	if shield_amm <= 0:
		shield_amm = 0
	bar_length = 100
	bar_height = 10
	fill = (shield_amm / 100) * bar_length
	outline_rect = pg.Rect(x, y, bar_length, bar_height)
	fill_rect = pg.Rect(x, y, fill, bar_height)
	pg.draw.rect(surf, GREEN, fill_rect)
	pg.draw.rect(surf, BLACK, outline_rect, 2)

def game_over():
	pass

#Classes
class Player(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = player_image
		self.rect = self.image.get_rect()
		self.rect.centerx = SCREENWIDTH/2
		self.rect.bottom = SCREENHEIGHT -6
		self.speedx = 1
		self.shoot_delay = 750
		self.last_shot = pg.time.get_ticks()
		self.shield = 100
		self.power_level = 1
		self.power_time = pg.time.get_ticks()

	def update(self):
		#imeout for powerups
		if self.power_level >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
			self.power_level -= 1
			self.power_time = pg.time.get_ticks()

		self.speedx = 0
		keystate = pg.key.get_pressed()
		if keystate[pg.K_LEFT] or joystick.get_axis(0) == -1:
			self.speedx = -5
		if keystate[pg.K_RIGHT] or joystick.get_axis(0) > 0:
			self.speedx = 5
		if keystate[pg.K_SPACE] or joystick.get_button(0):
			self.shoot()
		self.rect.x += self.speedx
		if self.rect.right > SCREENWIDTH:
			self.rect.right = SCREENWIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def powerup(self):
		self.power_level += 1
		self.power_time = pg.time.get_ticks()

	def shoot(self):
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if self.power_level >= 2:
				bullet1 = Bullet(self.rect.left + 11, self.rect.centery)
				bullet2 = Bullet(self.rect.right - 10, self.rect.centery)
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)
			else:
				bullet = Bullet(self.rect.centerx, self.rect.top)
				all_sprites.add(bullet)
				bullets.add(bullet)
			shoot_sound.play()

class Bullet(pg.sprite.Sprite):
	def __init__(self, x ,y):
		pg.sprite.Sprite.__init__(self)
		self.image = bullet_image
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -5

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class MobBullet(Bullet):
	"""Inherant class"""
	def __init__(self, x, y):
		super().__init__(x, y)
		self.image = mob_bullet_image
		self.rect.top = y
		self.speedy = 6

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > SCREENHEIGHT:
			self.kill()
	

class Mob(pg.sprite.Sprite):
	direction = True
	def __init__(self, x, y, move_delay):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(mob_images[0], (50, 64))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.speedx = 5
		self.direction = True
		self.frame = 0
		self.move_delay = move_delay
		self.move_last_update = pg.time.get_ticks()
		self.frame_rate = 100
		self.img_last_update = pg.time.get_ticks()
		self.sound = True

	def update(self):
		#Change image
		img_now = pg.time.get_ticks()
		if img_now - self.img_last_update >= self.frame_rate:
			self.img_last_update = img_now			
			if self.frame == len(mob_images):		
				self.frame = 0
			self.image = pg.transform.scale(mob_images[self.frame], (50, 64))
			self.frame += 1

		#Move mob	
		move_now = pg.time.get_ticks()
		if move_now - self.move_last_update > self.move_delay:
			self.move_last_update = move_now
			if self.direction:
				self.rect.x += self.speedx
			else:
				self.rect.x -= self.speedx
			if self.sound:
				enemy_sounds[0].play()
				self.sound = False	
			else:
				enemy_sounds[3].play()	
				self.sound = True

			#Spawn a bullet
			if random.random() >= 0.98:
				self.shoot()

	def shoot(self):
		mob_bullet = MobBullet(self.rect.centerx, self.rect.bottom)
		all_sprites.add(mob_bullet)
		mob_bullets.add(mob_bullet)

class BigEnemy(Mob):
	"""Inherant class"""
	def __init__(self, x, y, move_delay):
		super().__init__(x, y, move_delay)
		self.image = pg.transform.scale(bigenemy_images[0], (50, 50))
		self.frame_rate = 50

	def update(self):
		#Interate through images
		img_now = pg.time.get_ticks()
		if img_now - self.img_last_update >= self.frame_rate:
			self.img_last_update = img_now			
			if self.frame == len(bigenemy_images):		
				self.frame = 0
			self.image = pg.transform.scale(bigenemy_images[self.frame], (50, 50))
			self.frame += 1

		#Change direction
		move_now = pg.time.get_ticks()
		if move_now - self.move_last_update > self.move_delay:
			self.move_last_update = move_now
			if self.direction:
				self.rect.x += self.speedx
			else:
				self.rect.x -= self.speedx
			if self.sound:
				enemy_sounds[0].play()
				self.sound = False	
			else:
				enemy_sounds[3].play()	
				self.sound = True

			#Spawn a bullet
			if random.random() >= 0.99:
				self.shoot()

class Boss(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.scale(boss_img, (50, 66))
		self.rect = self.image.get_rect()
		self.rect.x = SCREENWIDTH + 1
		self.rect.y = 20
		self.speedx = 2

	def update(self):
		self.rect.x -= self.speedx
		if self.rect.right < 0:
			self.kill()
			boss_sound.fadeout(600)

class PowerUp(pg.sprite.Sprite):
	def __init__(self,center):
		pg.sprite.Sprite.__init__(self)
		self.type = random.choice([0,1])
		self.image = powerup_images[self.type]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 5

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top >= SCREENHEIGHT + 1:
			self.kill()

class LifePowerUp(PowerUp):
	def __init__(self, center):
		super().__init__(center)
		self.image = powerup_images[2]

class Explosion(pg.sprite.Sprite):
	def __init__(self,center):
		pg.sprite.Sprite.__init__(self)
		#self.size = size ***use for dictionary of diff images!***
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.frame_rate = 25
		self.last_update = pg.time.get_ticks()

	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.last_update = now		
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				self.image = explosion_anim[self.frame]	
			self.frame += 1
		
#Screen drawing function
def redraw_game_window():
	win.blit(background_scaled, background_rect)	
	all_sprites.draw(win)
	draw_text(win, 'Player 1 score: ' + str(score), 22, 5, 5)
	draw_shields(win, 166, 6, player.shield)
	pg.display.update()


#Create instances of sprites
all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
mob_bullets = pg.sprite.Group()
mobs = pg.sprite.Group()
Bmobs = pg.sprite.Group()
bosses = pg.sprite.Group()
powerups = pg.sprite.Group()
player = Player()
all_sprites.add(player)
Bmobs_y_list = [70, 140]
for ypos in Bmobs_y_list:
	for i in range(10):
		bigenemy = BigEnemy(((i+1)*70)-15, ypos, move_delay)
		all_sprites.add(bigenemy)
		Bmobs.add(bigenemy)
mob_y_list = [210, 280, 350]
for ypos in mob_y_list:
	for i in range (10):
		newmob(((i+1)*70)-15, ypos, move_delay)

score=0
pg.mixer.music.play(loops=-1)


#Main game loop
game_on = True
while game_on:

	clock.tick(FPS)
	#Process input (Events)
	for event in pg.event.get():#exit loop
		if event.type == pg.QUIT:
			game_on = False
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				game_on = False	


	#Update
	all_sprites.update()


	#Spawn a boss randomly
	now = pg.time.get_ticks()
	if now - boss_last_update >= rand_delay:
		boss_last_update = now
		rand_delay = random.randrange(4600,22000)		
		add_boss()

	#Check to see if a bullet hit a mob
	score = enemy_hit(mobs, 10, score, False)	
	score = enemy_hit(Bmobs, 30, score, False)
	score = enemy_hit(bosses, 50, score, True)

	#Check to see if a bullet has hit the player
	hits = pg.sprite.spritecollide(player, mob_bullets, True)
	for hit in hits:
		player.shield -= random.randrange(10,30)
		if player.shield <= 0:
			#player.kill()
			game_on = False

	#Check to see if the player has hit a powerup
	hits = pg.sprite.spritecollide(player, powerups, True)
	for hit in hits:
		if hit.image == powerup_images[0]: #increase the guns	
			player.powerup()

		if hit.image == powerup_images[1]: #increase the shields
			if player.shield < 100:
				player.shield += random.randrange(10, 40)
				if player.shield > 100:
					player.shield = 100

		if hit.image == powerup_images[2]:
			#give an extra life if lives are less than three
			pass

	#Check if enemies have hit the walls
	now = pg.time.get_ticks()
	if now - last_update >= move_delay:
		last_update = now
		enemy_check(mobs)
		enemy_check(Bmobs)


	#Draw/render
	redraw_game_window()


pg.quit()
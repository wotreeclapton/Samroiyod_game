#Sprite classes for Samroiyod game import pygame as pg
import random
import pygame as pg
import methods as meth

class Spritesheet:
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert_alpha()

	def get_image(self, x, y, width, height):
		#Grab an image from the sheet
		image = pg.Surface((width, height), pg.SRCALPHA)
		image.blit(self.spritesheet, (0,0), (x, y, width, height))
		return image
 
class Player1(pg.sprite.Sprite):
	def __init__(self, xpos , game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = self.game.sprite_sheet.get_image(354, 256, 64, 64)
		self.rect = self.image.get_rect()
		self.rect.centerx = xpos
		self.rect.bottom = meth.SCREENHEIGHT - 6
		self.speedx = 1
		self.shoot_delay = 750
		self.last_shot = pg.time.get_ticks()
		self.shield = 100
		self.power_level = 1
		self.power_time = pg.time.get_ticks()
		self.lives = 1
		self.hidden = False
		self.hide_timer = pg.time.get_ticks()

	def update(self):
		#unhide if hidden
		if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = meth.SCREENWIDTH / 2
			self.rect.bottom = meth.SCREENHEIGHT - 6

		#timeout for powerups
		if self.power_level >= 2 and pg.time.get_ticks() - self.power_time > meth.POWERUP_TIME:
			self.power_level -= 1
			self.power_time = pg.time.get_ticks()

		self.speedx = 0

		keystate = pg.key.get_pressed()
		if keystate[pg.K_a]:
			self.speedx = -5
		if keystate[pg.K_s]:
			self.speedx = 5
		if keystate[pg.K_f]:
			self.shoot()
		try:
			if self.game.joystick.get_axis(0) == -1:
				self.speedx = -5
			if self.game.joystick.get_axis(0) > 0:
				self.speedx = 5
			if self.game.joystick.get_button(0):
				self.shoot()
		except AttributeError:
			pass

		self.rect.x += self.speedx
		if self.rect.right > meth.SCREENWIDTH:
			self.rect.right = meth.SCREENWIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def powerup(self):
		self.power_level += 1
		self.power_time = pg.time.get_ticks()

	def shoot(self):
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet_list = [Bullet(self.rect.centerx, self.rect.top, self.game),Bullet(self.rect.left + 11, self.rect.centery, self.game),Bullet(self.rect.right - 10, self.rect.centery, self.game)]
			if self.power_level >= 3:
				for bul in bullet_list:
					self.game.all_sprites.add(bul)
					self.game.bullets.add(bul)
			elif self.power_level == 2:
				for bul in bullet_list[1:3]:
					self.game.all_sprites.add(bul)
					self.game.bullets.add(bul)
			else:
				bullet = Bullet(self.rect.centerx, self.rect.top, self.game)
				self.game.all_sprites.add(bullet_list[0])
				self.game.bullets.add(bullet_list[0])
			self.game.shoot_sound.play()

	def hide(self):
		self.hidden = True
		self.hide_timer = pg.time.get_ticks()
		self.rect.center = (meth.SCREENWIDTH / 2, meth.SCREENHEIGHT + 200)

	def player_level_up_anim(self):
		#move player 1 px every frame
		while True:
			self.game.clock.tick(140)
			if self.rect.centerx < meth.SCREENWIDTH / 2:
				self.rect.centerx += 1
			elif self.rect.centerx > meth.SCREENWIDTH / 2:
				self.rect.centerx -= 1
			elif self.rect.centerx == meth.SCREENWIDTH/2:
				while True:
					self.game.clock.tick(160)
					if self.rect.top > meth.SCREENHEIGHT/2:
						self.rect.top -= 1
					else:
						break
					self.game.draw()
			if self.rect.centerx == meth.SCREENWIDTH/2 and self.rect.top == meth.SCREENHEIGHT/2:
				break	
			self.game.draw()

class Player2(Player1):
	"""docstring for Player2"""
	def __init__(self, xpos , game):
		super(Player2, self).__init__(xpos , game)
		self.image = self.game.sprite_sheet.get_image(408, 344, 64, 64)

	def update(self):
		self.speedx = 0
		keystate = pg.key.get_pressed()
		if keystate[pg.K_LEFT]:
			self.speedx = -5
		if keystate[pg.K_RIGHT]:
			self.speedx = 5
		if keystate[pg.K_KP0]:
			self.shoot()
		# try:
		# 	if self.game.joystick.get_axis(0) == -1:
		# 		self.speedx = -5
		# 	if self.game.joystick.get_axis(0) > 0:
		# 		self.speedx = 5
		# 	if self.game.joystick.get_button(0):
		# 		self.shoot()
		# except AttributeError:
		# 	pass

		self.rect.x += self.speedx
		if self.rect.right > meth.SCREENWIDTH:
			self.rect.right = meth.SCREENWIDTH
		if self.rect.left < 0:
			self.rect.left = 0		

class Bullet(pg.sprite.Sprite):
	def __init__(self, x ,y, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = self.game.sprite_sheet.get_image(346, 321, 10, 12)
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
	def __init__(self, x, y, game):
		super().__init__(x, y, game)
		self.image = self.game.sprite_sheet.get_image(339, 321, 5, 24)
		self.rect.top = y
		self.speedy = 6

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > meth.SCREENHEIGHT:
			self.kill()	

class Mob(pg.sprite.Sprite):
	direction = True
	def __init__(self, x, y, img_type, frame_rate, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.img_type = img_type
		self.load_images()
		self.image = self.mob_images[self.img_type][0]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		#self.speedx = 5
		#self.direction = True
		self.frame = 0
		self.move_last_update = pg.time.get_ticks()
		self.frame_rate = frame_rate
		self.img_last_update = pg.time.get_ticks()
		#self.sound = True

	def load_images(self):
		self.mob_images = {}
		self.mob_images['mob'] = [pg.transform.scale(self.game.sprite_sheet.get_image(0, 272, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 272, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 272, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 272, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 272, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(0, 358, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 358, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 358, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 358, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 358, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(0, 445, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 445, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 445, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 445, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 445, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(0, 532, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 532, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 532, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 532, 64, 80), (50, 64)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 532, 64, 80), (50, 64))]

		self.mob_images['Bmob'] = [pg.transform.scale(self.game.sprite_sheet.get_image(0, 0, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 0, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 0, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 0, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 0, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(0, 68, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 68, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 68, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 68, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 68, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(0, 135, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 135, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 135, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 135, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 135, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(0, 205, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(68, 205, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(135, 205, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(203, 205, 64, 64), (50, 50)),
						   pg.transform.scale(self.game.sprite_sheet.get_image(272, 205, 64, 64), (50, 50))]

	def update(self):
		#Change image
		img_now = pg.time.get_ticks()
		if img_now - self.img_last_update >= self.frame_rate:
			self.img_last_update = img_now			
			if self.frame == len(self.mob_images[self.img_type]):		
				self.frame = 0
			self.image = self.mob_images[self.img_type][self.frame]
			self.frame += 1

		#Move mob	
		move_now = pg.time.get_ticks()
		if move_now - self.move_last_update > self.game.move_delay:
			self.move_last_update = move_now
			if self.game.mob_direction:
				self.rect.x += self.game.speedx
			else:
				self.rect.x -= self.game.speedx

			#Spawn a bullet
			if self.game.player1.alive():
				if random.random() >= 0.98:
					self.shoot()

	def shoot(self):
		mob_bullet = MobBullet(self.rect.centerx, self.rect.bottom, self.game)
		self.game.all_sprites.add(mob_bullet)
		self.game.mob_bullets.add(mob_bullet)

class StartMob(Mob):
	"""Inherant class"""
	def __init__(self, x, y, img_type, frame_rate, game):
		super(StartMob, self).__init__(x, y, img_type, frame_rate, game)

	def update(self):
		#Change image
		img_now = pg.time.get_ticks()
		if img_now - self.img_last_update >= self.frame_rate:
			self.img_last_update = img_now			
			if self.frame == len(self.mob_images[self.img_type]):		
				self.frame = 0
			if self.img_type == "Bmob": #Change image size if big mob
				self.image = pg.transform.scale(self.mob_images[self.img_type][self.frame], (64, 64))
				self.frame += 1
			else:
				self.image = self.mob_images[self.img_type][self.frame]
				self.frame += 1
		

class Boss(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self. game = game
		self.image = pg.transform.scale(self.game.sprite_sheet.get_image(497 , 256, 72, 96), (50, 66))
		self.rect = self.image.get_rect()
		self.rect.x = meth.SCREENWIDTH + 1
		self.rect.y = 28
		self.speedx = 2

	def update(self):
		self.rect.x -= self.speedx
		if self.rect.right < 0:
			self.kill()
			self.game.boss_sound.fadeout(600)

class PowerUp(pg.sprite.Sprite):
	def __init__(self,center, img_type, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.img_type = img_type
		self.type = random.choice([0,1])
		self.load_images()
		self.image = self.powerup_images[self.img_type][self.type]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 5

	def load_images(self):
		self.powerup_images = {}
		self.powerup_images['norm'] = [pg.transform.scale(self.game.sprite_sheet.get_image(425, 290, 28, 46), (15, 24)), pg.transform.scale(self.game.sprite_sheet.get_image(459, 256, 32, 30), (24, 26))]
		self.powerup_images['boss'] = [pg.transform.scale(self.game.sprite_sheet.get_image(458, 291, 32, 32), (24, 25)),  pg.transform.scale(self.game.sprite_sheet.get_image(425, 256, 32, 32), (24, 24))]

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top >= meth.SCREENHEIGHT + 1:
			self.kill()
			
class Explosion(pg.sprite.Sprite):
	def __init__(self, center, size, fr_rate, game):
		pg.sprite.Sprite.__init__(self)
		#self.size = size ***use for dictionary of diff images!***
		self. game = game
		self.size =size
		self.load_images()
		self.image = self.explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.frame_rate = fr_rate
		self.last_update = pg.time.get_ticks()

	def load_images(self):
		self.explosion_anim = {}
		self.explosion_anim['lg'] = [self.game.sprite_sheet.get_image(342, 0, 64, 64),
							   self.game.sprite_sheet.get_image(406, 0, 64, 64),
							   self.game.sprite_sheet.get_image(470, 0, 64, 64),
							   self.game.sprite_sheet.get_image(534, 0, 64, 64),
							   self.game.sprite_sheet.get_image(342, 64, 64, 64),
							   self.game.sprite_sheet.get_image(406, 64, 64, 64),
							   self.game.sprite_sheet.get_image(470, 64, 64, 64),
							   self.game.sprite_sheet.get_image(534, 64, 64, 64),
							   self.game.sprite_sheet.get_image(342, 128, 64, 64),
							   self.game.sprite_sheet.get_image(406, 128, 64, 64),
							   self.game.sprite_sheet.get_image(470, 128, 64, 64),
							   self.game.sprite_sheet.get_image(534, 128, 64, 64),
							   self.game.sprite_sheet.get_image(342, 192, 64, 64),
							   self.game.sprite_sheet.get_image(406, 192, 64, 64),
							   self.game.sprite_sheet.get_image(470, 192, 64, 64),
							   self.game.sprite_sheet.get_image(534, 192, 64, 64)]

		self.explosion_anim['sm'] = [pg.transform.scale(self.game.sprite_sheet.get_image(342, 0, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(406, 0, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(470, 0, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(534, 0, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(342, 64, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(406, 64, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(470, 64, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(534, 64, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(342, 128, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(406, 128, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(470, 128, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(534, 128, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(342, 192, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(406, 192, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(470, 192, 64, 64), (32, 32)),
							   pg.transform.scale(self.game.sprite_sheet.get_image(534, 192, 64, 64), (32, 32))]

		self.explosion_anim['boss'] = [pg.transform.scale(self.game.sprite_sheet.get_image(344, 404, 128, 128), (192, 192)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(435, 404, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(532, 404, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(633, 404, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(734, 404, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(344, 501, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(451, 501, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(559, 501, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(672, 501, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(344, 607, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(460, 607, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(577, 607, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(696, 607, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(578, 305, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(704, 305, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(578, 202, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(702, 202, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(604, 98, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(735, 98, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(604, 0, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(735, 0, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(0, 618, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(133, 618, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(0, 727, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(133, 727, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(271, 727, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(406, 727, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(547, 727, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(681, 727, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(0, 834, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(133, 834, 128, 128), (210, 210)),
								   pg.transform.scale(self.game.sprite_sheet.get_image(271, 834, 128, 128), (210, 210))
								   ]

	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.last_update = now		
			if self.frame == len(self.explosion_anim[self.size]):
				self.kill()
			else:
				self.image = self.explosion_anim[self.size][self.frame]	
			self.frame += 1


class StartButtons(pg.sprite.Sprite):
	"""docstring for StartButtons"""
	def __init__(self, button_type, button_center, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.load_images()
		self.button_type = button_type
		self.button_center = button_center
		self.image = self.buttons[self.button_type][0]
		self.rect = self.image.get_rect()
		self.rect.center = button_center


	def load_images(self):
		self.buttons = {1:[self.game.sprite_sheet.get_image(562, 858, 146, 41), self.game.sprite_sheet.get_image(402, 858, 157, 44)]
		, 2:[self.game.sprite_sheet.get_image(562, 905, 146, 41), self.game.sprite_sheet.get_image(402, 905, 157, 44)]}

	def update(self):
		if self.game.number_of_players == 2 and self.button_type == 2:
			self.image = self.buttons[self.button_type][1]
		elif self.game.number_of_players > 0 and self.button_type == 1:
			self.image = self.buttons[self.button_type][1]
		else:
			self.image = self.buttons[self.button_type][0]
		self.rect = self.image.get_rect()
		self.rect.center = self.button_center
		

			

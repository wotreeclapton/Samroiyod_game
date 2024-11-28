#! python 3
'''
SAMROIYOD GAME SPRITES developed by Mr Steven J walden
    Nov. 2020
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND
[See License.txt file]
'''

import random
import pygame as pg
import methods as meth
import constants as const

class Spritesheet:
	def __init__(self, filename):
		# self.game = game
		# self.spritesheet = self.game.resource_manager.get_image(filename)
		self.spritesheet = pg.image.load(filename)

	def get_image(self, x, y, width, height):
		#Grab an image from the sheet
		image = pg.Surface((width, height), pg.SRCALPHA)
		image.blit(self.spritesheet, (0,0), (x, y, width, height))
		return image


class Player1(pg.sprite.Sprite):
	def __init__(self, xpos , game):
		super().__init__()
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("player1")
		self.rect = self.image.get_rect()
		self.rect.centerx = xpos
		self.rect.bottom = const.SCREENHEIGHT - 6
		self.shoot_sound = pg.mixer.Sound(
			self.game.resource_manager.get_sound("shoot_sound"))
		self.shoot_sound.set_volume(0.04)
		self.speedx = 1
		self.shoot_delay = 750
		self.last_shot = pg.time.get_ticks()
		self.shield = 100
		self.power_level = 1
		self.power_time = pg.time.get_ticks()
		self.active_shield = False
		self.active_shield_time = pg.time.get_ticks()
		self.lives = 1
		self.hidden = False
		self.hide_timer = pg.time.get_ticks()

	def update(self):
		self.player_hidden_check()
		self.powerup_timeout_check()
		self.shield_timeout_check()

		self.speedx = 0

		keystate = pg.key.get_pressed()
		if keystate[pg.K_a]:
			self.speedx = -5
		if keystate[pg.K_s]:
			self.speedx = 5
		if keystate[pg.K_f]:
			self.shoot(player_bull_list=self.game.player1_bullets)
		try:
			if self.game.joystick1.get_axis(0) == -1:
				self.speedx = -5
			if self.game.joystick1.get_axis(0) > 0:
				self.speedx = 5
			if self.game.joystick1.get_button(2):
				self.shoot(player_bull_list=self.game.player1_bullets)
		except AttributeError:
			pass

		self.rect.x += self.speedx
		self.screen_edge_check()

	def screen_edge_check(self):
		if self.rect.right > const.SCREENWIDTH:
			self.rect.right = const.SCREENWIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def player_hidden_check(self):
		if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = const.SCREENWIDTH / 2
			self.rect.bottom = const.SCREENHEIGHT - 6

	def shield_timeout_check(self):
		if self.active_shield == True and pg.time.get_ticks() - self.active_shield_time > const.POWERUP_TIME:
			self.active_shield = False
			self.power_time = pg.time.get_ticks()

	def	powerup_timeout_check(self):
		if self.power_level >= 2 and pg.time.get_ticks() - self.power_time > const.POWERUP_TIME:
			self.power_level -= 1
			self.power_time = pg.time.get_ticks()

	def powerup(self):
		self.power_level += 1
		self.power_time = pg.time.get_ticks()

	def shieldup(self):
		self.active_shield = True
		self.active_shield_time = pg.time.get_ticks()

	def shoot(self, player_bull_list):
		now = pg.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			if player_bull_list == self.game.player2_bullets:
				self.bullet_list = [Player2Bullet(self.rect.centerx, self.rect.top, self.game),Player2Bullet(self.rect.left + 11, self.rect.centery, self.game),Player2Bullet(self.rect.right - 10, self.rect.centery, self.game)]
			else:
				self.bullet_list = [Player1Bullet(self.rect.centerx, self.rect.top, self.game),Player1Bullet(self.rect.left + 11, self.rect.centery, self.game),Player1Bullet(self.rect.right - 10, self.rect.centery, self.game)]
			if self.power_level >= 3:
				for bul in self.bullet_list:
					self.game.all_sprites.add(bul)
					player_bull_list.add(bul)
			elif self.power_level == 2:
				for bul in self.bullet_list[1:3]:
					self.game.all_sprites.add(bul)
					player_bull_list.add(bul)
			else:
				self.game.all_sprites.add(self.bullet_list[0])
				player_bull_list.add(self.bullet_list[0])
			self.shoot_sound.play()

	def hide(self):
		self.hidden = True
		self.hide_timer = pg.time.get_ticks()
		self.rect.center = (const.SCREENWIDTH / 2, const.SCREENHEIGHT + 200)

	def death_check(self, hit):
		self.expl = Explosion(hit, "boss", 100, self.game)


class Player2(Player1):
	"""docstring for Player2"""
	def __init__(self, xpos , game):
		super(Player2, self).__init__(xpos , game)
		self.image = self.game.resource_manager.get_sprite_image("player2")

	def update(self):
		self.speedx = 0
		keystate = pg.key.get_pressed()
		if keystate[pg.K_LEFT]:
			self.speedx = -5
		if keystate[pg.K_RIGHT]:
			self.speedx = 5
		if keystate[pg.K_KP0]:
			self.shoot(player_bull_list=self.game.player2_bullets)
		try:
			if self.game.joystick2.get_axis(0) == -1:
				self.speedx = -5
			if self.game.joystick2.get_axis(0) > 0:
				self.speedx = 5
			if self.game.joystick2.get_button(0):
				self.shoot(player_bull_list=self.game.player2_bullets)
		except AttributeError:
			pass

		self.rect.x += self.speedx
		"""Check if works from player 1 code"""
		# if self.rect.right > const.SCREENWIDTH:
		# 	self.rect.right = const.SCREENWIDTH
		# if self.rect.left < 0:
		# 	self.rect.left = 0


class LevelUpPlayer1(pg.sprite.Sprite):
	def __init__(self, game):
		super().__init__()
		#Player sprite to use in level up animation
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("player1")
		self.rect = self.image.get_rect()
		self.rect.centerx  = -40
		self.rect.bottom = const.SCREENHEIGHT - 6
		self.end_poss = const.SCREENWIDTH/2

	def update(self):
		# move the player to the middle x
		if self.rect.centerx < self.end_poss:
			self.rect.centerx += 2
		elif self.rect.centerx > self.end_poss:
			self.rect.centerx -= 2
		else:
			# Move the player half way up the screen
			if self.rect.top > const.SCREENHEIGHT/2:
				self.rect.top -= 2
			else:
				self.end_poss = const.SCREENWIDTH/2
				self.rect.bottom = const.SCREENHEIGHT - 6
				self.game.change_state("play")


class LevelUpPlayer2(LevelUpPlayer1):
	def __init__(self, game):
		super().__init__(game)
		#Player sprite to use in level up animation
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("player2")
		# self.rect = self.image.get_rect()
		self.rect.centerx = const.SCREENWIDTH + 40

	def update(self):
		pass


class Player1Bullet(pg.sprite.Sprite):
	def __init__(self, x ,y, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("player1_bullet")
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -5

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


class Player2Bullet(Player1Bullet):
	"""docstring for Player2Bullet"""
	def __init__(self, x ,y, game):
		super(Player2Bullet, self).__init__(x ,y, game)
		self.image = self.game.resource_manager.get_sprite_image("player2_bullet")


class MobBullet(Player1Bullet):
	"""Inherant class"""
	def __init__(self, x, y, game):
		super().__init__(x, y, game)
		# self.image = self.game.sprite_sheet.get_image(339, 321, 5, 24)
		self.image = self.game.resource_manager.get_sprite_image("invader_bullet")
		self.rect.top = y
		self.speedy = 6

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top > const.SCREENHEIGHT:
			self.kill()	


class Mob(pg.sprite.Sprite):
	direction = True
	def __init__(self, x, y, img_type, frame_rate, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.img_type = img_type
		self.image = self.game.resource_manager.get_sprite_image(f"{self.img_type}_enemy1")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.frame = 1
		self.move_last_update = pg.time.get_ticks()
		self.frame_rate = frame_rate
		self.img_last_update = pg.time.get_ticks()
		#self.sound = True

	def update(self):
		#Change image
		img_now = pg.time.get_ticks()
		if img_now - self.img_last_update >= self.frame_rate:
			self.img_last_update = img_now
			if self.frame == 21:
				self.frame = 1
			self.image = self.game.resource_manager.get_sprite_image(
				f"{self.img_type}_enemy{self.frame}")
			self.frame += 1

		#Move mob
		move_now = pg.time.get_ticks()
		if move_now - self.move_last_update > self.game.enemy_checks.move_delay:
			self.move_last_update = move_now
			# if self.game.mob_direction:
			if self.game.enemy_checks.mob_direction: #Checks direction of mobs from CheckEnemy class
				self.rect.x += self.game.enemy_checks.speedx
			else:
				self.rect.x -= self.game.enemy_checks.speedx

			#Spawn a bullet
			if len(self.game.player_group) > 0:
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
			if self.frame == 21:
				self.frame = 1
			if self.img_type == "ep": #Change image size if big mob
				self.image = pg.transform.scale(self.game.resource_manager.get_sprite_image(
                            f"{self.img_type}_enemy{self.frame}"), (64, 64))
				self.frame += 1
			else:
				self.image = self.game.resource_manager.get_sprite_image(
                                    f"{self.img_type}_enemy{self.frame}")
				self.frame += 1


class Boss(pg.sprite.Sprite):
	def __init__(self, game):
		pg.sprite.Sprite.__init__(self)
		self. game = game
		self.image = self.game.resource_manager.get_sprite_image("boss")
		self.rect = self.image.get_rect()
		self.rect.x = const.SCREENWIDTH + 1
		self.rect.y = 28
		self.sound = self.game.resource_manager.get_sound("boss_enemy_sound")
		self.sound.set_volume(0.2)
		self.channel = pg.mixer.Channel(0)
		self.channel.play(self.sound, -1)
		self.speedx = 2

	def update(self):
		self.rect.x -= self.speedx
		if self.rect.right < 0:
			self.kill()
			self.sound.fadeout(600)


class HyperMob(Mob):
	"""docstring for HyperMob"""
	def __init__(self, x, y, img_type, frame_rate, game):
		super(HyperMob, self).__init__(x, y, img_type, frame_rate, game)
		self.image_orig	= img_type
		self.image = self.image_orig.copy()
		#self.image.fill(red)
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width *.85 /2)
		#pygame.draw.circle(self.image, red, self.rect.center, self.radius)	
		self.rect.x = random.randrange(const.SCREENWIDTH - self.rect.width)
		self.rect.y = random.randrange(-150,-100)
		self.speedy = random.randrange(1,8)
		self.speedx = random.randrange(-3,3)
		self.rot = 0
		self.rot_speed = random.randrange(-8, 8)
		self.last_update = pg.time.get_ticks()

	def rotate(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = self.rot + self.rot_speed % 360
			new_image = pg.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > const.SCREENHEIGHT + 10 or self.rect.left < -25 or self.rect.right > const.SCREENWIDTH + 20:
			self.rect.x = random.randrange(const.SCREENWIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,8)


class PowerUp(pg.sprite.Sprite):
	def __init__(self,center, img_type, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.type = random.choice([1,2])
		self.image = self.game.resource_manager.get_sprite_image(f"powerup_{img_type}{self.type}")
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 5

	def update(self):
		self.rect.y += self.speedy
		if self.rect.top >= const.SCREENHEIGHT + 1:
			self.kill()

		# Check for powerup collect
		hit = pg.sprite.collide_circle(self, self.game.player1)
		if hit:
			self.powerup_collect(self.game.player1)

		if all(item is True for item in self.game.players):
			hit = pg.sprite.collide_circle(self, self.game.player2)
			if hit:
				self.powerup_collect(self.game.player2)
			
	def powerup_collect(self, player):
		#Extra guns
		if self.image == self.game.resource_manager.get_sprite_image("powerup_norm1"):
			self.game.resource_manager.get_sound("powerup_gun_sound").play()
			player.powerup()

		#Extra shield
		if self.image == self.game.resource_manager.get_sprite_image("powerup_norm2"):
			self.game.resource_manager.get_sound("powerup_shield_sound").play()
			player.shieldup()

		#Extra life
		if self.image == self.game.resource_manager.get_sprite_image("powerup_boss1"):
			self.game.resource_manager.get_sound("powerup_life_sound").play()
			if player.lives < 3:
				player.lives += 1
		
		#Starts hyperspace
		if self.image == self.game.resource_manager.get_sprite_image("powerup_boss2"):
			self.game.resource_manager.get_sound("powerup_hyperspace_sound").play()
			# self.game.hyperspace() 

		self.kill()


class Explosion(pg.sprite.Sprite):
	def __init__(self, center, img_type, fr_rate, game, snd_type):
		pg.sprite.Sprite.__init__(self)
		#self.size = size ***use for dictionary of diff images!***
		self. game = game
		self.img_type = img_type
		self.image = self.game.resource_manager.get_sprite_image(f"{self.img_type}_explosion1")
		self.rect = self.image.get_rect()
		self.rect.center = center
		if snd_type == "mob": #Normal mob explosion sound
			self.sound = self.game.resource_manager.get_sound("mob_explosion_sound")
			self.sound.set_volume(0.04)
		elif snd_type == "death": #Final player death explosion sound
			self.sound = self.game.resource_manager.get_sound("death_sound")
			self.sound.set_volume(0.5)			
		elif snd_type == "boss": #Boss explosion sound
			self.sound = self.game.resource_manager.get_sound(
				f"explosion{random.randint(1, 2)}_sound")
		self.sound.play()
		self.frame = 1
		self.frame_rate = fr_rate
		self.last_update = pg.time.get_ticks()

	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.last_update = now
			if self.img_type == "boss":
				if self.frame == 33:
					self.kill()
				else:
					self.image = self.game.resource_manager.get_sprite_image(
						f"{self.img_type}_explosion{self.frame}")
			elif self.frame == 17:
				self.kill()
			else:
				self.image = self.game.resource_manager.get_sprite_image(
                            f"{self.img_type}_explosion{self.frame}")
			self.frame += 1


class Shield1(pg.sprite.Sprite):
	"""docstring for shield"""
	def __init__(self, xpos, game):
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = self.game.resource_manager.get_sprite_image("shield1")
		self.rect = self.image.get_rect()
		self.rect.centerx = xpos
		self.rect.bottom = const.SCREENHEIGHT - 6
		self.frame = 1
		self.frame_rate = 36
		self.last_update = pg.time.get_ticks()
		self.speedx = 0

	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.last_update = now
			if self.frame == 4:
				self.frame = 1
				self.kill()
			self.image = self.game.resource_manager.get_sprite_image(f"shield{self.frame}")
			self.frame += 1
		self.rect = self.image.get_rect()
		self.rect.centerx = self.game.player1.rect.centerx
		self.rect.bottom = const.SCREENHEIGHT - 6


class Shield2(Shield1):
	"""docstring for Shield2"""
	def __init__(self, xpos, game):
		super(Shield2, self).__init__(xpos, game)
		
	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.last_update = now
			if self.frame == 4:
				self.frame = 1
				self.kill()
			self.image = self.game.resource_manager.get_sprite_image(f"shield{self.frame}")
			self.frame += 1
		self.rect = self.image.get_rect()
		self.rect.centerx = self.game.player2.rect.centerx
		self.rect.bottom = const.SCREENHEIGHT - 6		


class FlashingSprite(pg.sprite.Sprite):
    def __init__(self, image, rect, flash_interval=500):
        super().__init__()
        self.original_image = image
        self.transparent_image = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
        self.transparent_image.fill((0, 0, 0, 0))
        self.image = self.original_image
        self.rect = rect
        self.flash_interval = flash_interval
        self.last_flash_time = pg.time.get_ticks()
        self.visible = True

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_flash_time >= self.flash_interval:
            self.visible = not self.visible
            self.last_flash_time = current_time
        self.image = self.original_image if self.visible else self.transparent_image

import pygame as pg
import constants as const
from os import path
import constants as const


class ResourceManager:
	def __init__(self):
		self.images = {}
		self.sprite_images = {}
		self.sounds = {}
		self.music = {}

	def load_image(self, name, filename, scale=None, convert_mode=None):
		# Load an image from the image folder and optionally scale it.
		image_path = path.join(const.IMAGE_FOLDER, filename)
		try:
			image = pg.image.load(image_path)

			# Apply conversion mode
			if convert_mode == "convert":
				image = image.convert()
			elif convert_mode == "convert_alpha":
				image = image.convert_alpha()

			# Scale the image if needed
			if scale:
				image = pg.transform.scale(image, scale)

			self.images[name] = image
		except pg.error as e:
			print(f"Error loading image {filename}: {e}")

	def get_image(self, name):
		# Retrieves a loaded image.
		return self.images.get(name)
	
	def load_spritesheet_image(self, name, x, y, width, height, scale=None):
		#Retrieves an image from the spritesheet
		image = pg.Surface((width, height), pg.SRCALPHA)
		image.blit(self.images.get(name), (0, 0), (x, y, width, height))
		# Scale the image if needed
		if scale:
			image = pg.transform.scale(image, scale)

		return image
	
	def get_sprite_image(self, name):
		#returns a sprite image.
		return self.sprite_images.get(name)
	
	def load_sound(self, name, filename):
		# Load a sound from the specified folder.
		sound_path = path.join(const.SOUND_FOLDER, filename)
		try:
			self.sounds[name] = pg.mixer.Sound(sound_path)
		except pg.error as e:
			print(f"Error loading sound {filename}: {e}")

	def get_sound(self, name):
		# Retrieves a loaded sound.
		sound = self.sounds.get(name)
		if sound is None:
			raise ValueError(
				f"Sound '{name}' not found. Make sure it is loaded correctly.")
		return sound

	def load_music(self, name, filename):
		# Load a music file path.
		music_path = path.join(const.SOUND_FOLDER, filename)
		if path.exists(music_path):
			self.music[name] = music_path
		else:
			print(f"Error: Music file {filename} not found.")

	def get_music(self, name):
		# Retrieve the path of a loaded music file.
		return self.music.get(name)

	def load_all_resources(self):
		# Load all images and sounds
		self.load_images()
		self.load_sounds()
		self.load_music_files()

	def load_images(self):
		# Load all images
		images_with_alpha = [
			("spritesheet", "Samroiyodgame_img_sheet.png")
		]

		images_without_alpha = [
			("start_screen", "start_screen.jpg", (const.SCREENWIDTH, const.SCREENHEIGHT)),
			("game_screen", "SchoolBg.jpg", (const.SCREENWIDTH, const.SCREENHEIGHT)),
			("gameover_screen", "game_over_screen.jpg", (const.SCREENWIDTH, const.SCREENHEIGHT))
			]
		
		images_from_spritesheet = [
			("player1", (354, 256), (64, 64)),
			("player2", (408, 339), (64, 64)),
			("player1_start_images", (0, 965), (243, 45)),
			("player2_start_images", (0, 1014), (243, 45)),
			("player1_bullet", (346, 321), (10, 12)),
			("player2_bullet", (358, 321), (10, 12)),
			("invader_bullet", (339, 321), (5, 24)),
			("boss", (497, 256), (72, 96), (50, 66)),
			("powerup_norm1", (425, 290), (28, 46), (15, 24)),
			("powerup_norm2", (459, 256), (32, 30), (24, 26)),
			("powerup_boss1", (458, 291), (32, 32), (24, 25)),
			("powerup_boss2", (425, 256), (32, 32), (24, 24)),
			("shield1", (0, 1064), (133, 78)),
			("shield2", (138, 1064), (144, 84)),
			("shield3", (285, 1064), (144, 84)),
			("1up_button_small", (406, 907), (146, 41)),
			("2up_button_small", (580, 859), (146, 41)),
			("1up_button_large", (402, 858), (157, 44)),
			("2up_button_large", (572, 906), (157, 44)),
			("press_to_start", (248, 964), (379, 58)),
			("pause_image", (640, 964), (207, 57)),
			("samroy_enemy1", (0, 272), (64, 80), (50, 64)),
			("samroy_enemy2", (68, 272), (64, 80), (50, 64)),
			("samroy_enemy3", (135, 272), (64, 80), (50, 64)),
			("samroy_enemy4", (203, 272), (64, 80), (50, 64)),
			("samroy_enemy5", (272, 272), (64, 80), (50, 64)),
			("samroy_enemy6", (0, 358), (64, 80), (50, 64)),
			("samroy_enemy7", (68, 358), (64, 80), (50, 64)),
			("samroy_enemy8", (135, 358), (64, 80), (50, 64)),
			("samroy_enemy9", (203, 358), (64, 80), (50, 64)),
			("samroy_enemy10", (272, 358), (64, 80), (50, 64)),
			("samroy_enemy11", (0, 445), (64, 80), (50, 64)),
			("samroy_enemy12", (68, 445), (64, 80), (50, 64)),
			("samroy_enemy13", (135, 445), (64, 80), (50, 64)),
			("samroy_enemy14", (203, 445), (64, 80), (50, 64)),
			("samroy_enemy15", (272, 445), (64, 80), (50, 64)),
			("samroy_enemy16", (0, 532), (64, 80), (50, 64)),
			("samroy_enemy17", (68, 532), (64, 80), (50, 64)),
			("samroy_enemy18", (135, 532), (64, 80), (50, 64)),
			("samroy_enemy19", (203, 532), (64, 80), (50, 64)),
			("samroy_enemy20", (272, 532), (64, 80), (50, 64)),
			("ep_enemy1", (0, 0), (64, 64), (50, 50)),
			("ep_enemy2", (68, 0), (64, 64), (50, 50)),
			("ep_enemy3", (135, 0), (64, 64), (50, 50)),
			("ep_enemy4", (203, 0), (64, 64), (50, 50)),
			("ep_enemy5", (272, 0), (64, 64), (50, 50)),
			("ep_enemy6", (0, 68), (64, 64), (50, 50)),
			("ep_enemy7", (68, 68), (64, 64), (50, 50)),
			("ep_enemy8", (135, 68), (64, 64), (50, 50)),
			("ep_enemy9", (203, 68), (64, 64), (50, 50)),
			("ep_enemy10", (272, 68), (64, 64), (50, 50)),
			("ep_enemy11", (0, 135), (64, 64), (50, 50)),
			("ep_enemy12", (68, 135), (64, 64), (50, 50)),
			("ep_enemy13", (135, 135), (64, 64), (50, 50)),
			("ep_enemy14", (203, 135), (64, 64), (50, 50)),
			("ep_enemy15", (272, 135), (64, 64), (50, 50)),
			("ep_enemy16", (0, 205), (64, 64), (50, 50)),
			("ep_enemy17", (68, 205), (64, 64), (50, 50)),
			("ep_enemy18", (135, 205), (64, 64), (50, 50)),
			("ep_enemy19", (203, 205), (64, 64), (50, 50)),
			("ep_enemy20", (272, 205), (64, 64), (50, 50)),
			("sm_explosion1", (342, 0), (64, 64), (32, 32)),
			("sm_explosion2", (406, 0), (64, 64), (32, 32)),
			("sm_explosion3", (470, 0), (64, 64), (32, 32)),
			("sm_explosion4", (534, 0), (64, 64), (32, 32)),
			("sm_explosion5", (342, 64), (64, 64), (32, 32)),
			("sm_explosion6", (406, 64), (64, 64), (32, 32)),
			("sm_explosion7", (470, 64), (64, 64), (32, 32)),
			("sm_explosion8", (534, 64), (64, 64), (32, 32)),
			("sm_explosion9", (342, 128), (64, 64), (32, 32)),
			("sm_explosion10", (406, 128), (64, 64), (32, 32)),
			("sm_explosion11", (470, 128), (64, 64), (32, 32)),
			("sm_explosion12", (534, 128), (64, 64), (32, 32)),
			("sm_explosion13", (342, 192), (64, 64), (32, 32)),
			("sm_explosion14", (406, 192), (64, 64), (32, 32)),
			("sm_explosion15", (470, 192), (64, 64), (32, 32)),
			("sm_explosion16", (534, 192), (64, 64), (32, 32)),
			("lg_explosion1", (342, 0), (64, 64)),
			("lg_explosion2", (406, 0), (64, 64)),
			("lg_explosion3", (470, 0), (64, 64)),
			("lg_explosion4", (534, 0), (64, 64)),
			("lg_explosion5", (342, 64), (64, 64)),
			("lg_explosion6", (406, 64), (64, 64)),
			("lg_explosion7", (470, 64), (64, 64)),
			("lg_explosion8", (534, 64), (64, 64)),
			("lg_explosion9", (342, 128), (64, 64)),
			("lg_explosion10", (406, 128), (64, 64)),
			("lg_explosion11", (470, 128), (64, 64)),
			("lg_explosion12", (534, 128), (64, 64)),
			("lg_explosion13", (342, 192), (64, 64)),
			("lg_explosion14", (406, 192), (64, 64)),
			("lg_explosion15", (470, 192), (64, 64)),
			("lg_explosion16", (534, 192), (64, 64)),
			("boss_explosion1", (344, 404), (128, 128), (210, 210)),
			("boss_explosion2", (435, 404), (128, 128), (210, 210)),
			("boss_explosion3", (532, 404), (128, 128), (210, 210)),
			("boss_explosion4", (633, 404), (128, 128), (210, 210)),
			("boss_explosion5", (734, 404), (128, 128), (210, 210)),
			("boss_explosion6", (344, 501), (128, 128), (210, 210)),
			("boss_explosion7", (451, 501), (128, 128), (210, 210)),
			("boss_explosion8", (559, 501), (128, 128), (210, 210)),
			("boss_explosion9", (672, 501), (128, 128), (210, 210)),
			("boss_explosion10", (344, 607), (128, 128), (210, 210)),
			("boss_explosion11", (460, 607), (128, 128), (210, 210)),
			("boss_explosion12", (577, 607), (128, 128), (210, 210)),
			("boss_explosion13", (696, 607), (128, 128), (210, 210)),
			("boss_explosion14", (578, 305), (128, 128), (210, 210)),
			("boss_explosion15", (704, 305), (128, 128), (210, 210)),
			("boss_explosion16", (578, 202), (128, 128), (210, 210)),
			("boss_explosion17", (702, 202), (128, 128), (210, 210)),
			("boss_explosion18", (604, 98), (128, 128), (210, 210)),
			("boss_explosion19", (735, 98), (128, 128), (210, 210)),
			("boss_explosion20", (604, 0), (128, 128), (210, 210)),
			("boss_explosion21", (735, 0), (128, 128), (210, 210)),
			("boss_explosion22", (0, 618), (128, 128), (210, 210)),
			("boss_explosion23", (133, 618), (128, 128), (210, 210)),
			("boss_explosion24", (0, 727), (128, 128), (210, 210)),
			("boss_explosion25", (133, 727), (128, 128), (210, 210)),
			("boss_explosion26", (271, 727), (128, 128), (210, 210)),
			("boss_explosion27", (406, 727), (128, 128), (210, 210)),
			("boss_explosion28", (547, 727), (128, 128), (210, 210)),
			("boss_explosion29", (681, 727), (128, 128), (210, 210)),
			("boss_explosion30", (0, 834), (128, 128), (210, 210)),
			("boss_explosion31", (133, 834), (128, 128), (210, 210)),
			("boss_explosion32", (271, 834), (128, 128), (210, 210)),
		]
		
		# Load images that need convert()
		for name, filename, *scale in images_without_alpha:
			scale = scale[0] if scale else None
			self.load_image(name, filename, scale, convert_mode="convert")

		# Load images that need convert_alpha()
		for name, filename, *scale in images_with_alpha:
			scale = scale[0] if scale else None
			self.load_image(name, filename, scale, convert_mode="convert_alpha")

		#Load images from a spritesheet
		for name, coords, size, *scale in images_from_spritesheet:
			x , y= coords[0], coords[1]
			width, height = size[0], size[1]
			scale = scale[0] if scale else None
			image = self.load_spritesheet_image("spritesheet", x, y, width, height, scale)
			self.sprite_images[name] = image

	def load_sounds(self):
		# Load all sounds
		sound_data = [
			("shoot_sound", "bullet_shoot.wav"),
			("mob_explosion_sound", "enemy_killed.wav"),
			("high_score_sound", "new_highscore.ogg"),
			("boss_enemy_sound", "ufo_lowpitch.wav"),
			("powerup_gun_sound", "guns.wav"),
			("powerup_shield_sound", "shield.wav"),
			("powerup_life_sound", "extra_life.wav"),
			("powerup_hyperspace_sound", "hyperspace_collect.wav"),
			("explosion1_sound", "Explosion1.wav"),
			("explosion2_sound", "Explosion2.wav"),
			("death_sound", "death_explosion.wav")
		]

		for name, filename in sound_data:
			self.load_sound(name, filename)

	def load_music_files(self):
		# Load all music files.
		music_data = [
				("game_music", "tgfcoder-FrozenJam-SeamlessLoop.ogg"),
				("start_screen_music", "through_space.ogg")
			]

		for name, filename in music_data:
			self.load_music(name, filename)

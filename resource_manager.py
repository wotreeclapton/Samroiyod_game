import pygame as pg
import constants as const
from os import path


class ResourceManager:
	def __init__(self):
		self.images = {}
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

	def get_image(self):
		pass

	def load_sound(self):
		pass

	def get_sound(self):
		pass

	def load_music(self):
		pass

	def get_music(self):
		pass

	def load_all_resources(self):
		# Load all images and sounds
		self.load_images()
		self.load_sounds()
		self.load_music_files()

	def load_images(self):
		# Load all images
		images_with_alpha = []

		images_without_alpha = [
			("start_screen", "start_screen.jpg"),
			("game_screen", "SchoolBg.jpg"),
			("gameover_screen", "game_over_screen.jpg")
			]
		
		# Load images that need convert()
		for name, filename, *scale in images_without_alpha:
			scale = scale[0] if scale else None
			self.load_image(name, filename, convert_mode="convert")

	def load_sounds(self):
		pass

	def load_music_files(self):
		pass
"""
	SAMROIYOD GAME 	CONSTANTS developed by Mr Steven J walden
    Sept. 2024
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND

	Some of the sounds in this project were created by David McKee (ViRiX) soundcloud.com/virix

	[See License.txt file]
"""

from os import path

__AUTHOR__ = "Mr Steven J Walden"
__VERSION__ = "1.2.0"

GAMENAME = "Samroiyod invaders V"

GAME_FOLDER = path.dirname(__file__)
IMAGE_FOLDER = path.join(GAME_FOLDER, "img")
SOUND_FOLDER = path.join(GAME_FOLDER, "snd")
RESOURCES_FOLDER = path.join(GAME_FOLDER, "resources")

COMX = 380
COMY = 85
SCREENWIDTH = 800
SCREENHEIGHT = 780
FPS = 60
START_BUTTON1_X = SCREENWIDTH/2 - 87
START_BUTTON2_X = SCREENWIDTH/2 + 87
MUSIC_VOLUME = 1.0

HARLOW_FONT = "HARLOWSI.ttf"
OCRA_FONT = "OCRAEXT.ttf"

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

POWERUP_TIME = 10000
# MOVE_DELAY = 550

MOB_POSITIONS = {
    "Bmobs": [100, 166],  # Y-positions for big mobs
    "mobs": [227, 297, 367]  # Y-positions for smaller mobs
}

'''

'''

import pygame as pg
import random
import methods as meth
import constants as const
from game_state import GameState
from resource_manager import load_high_score
from level_change import LevelChange
from sprites import Mob, Boss

class PlayScreen(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.rand_delay = random.randrange(8400, 12000)
        self.last_update = pg.time.get_ticks()
        self.boss_last_update = pg.time.get_ticks()
        self.sound_last_update = pg.time.get_ticks()
        self.sound = True
        self.game_level = 1
        # self.boss = None  # Created first for pause game check
        self.played_high_score_sound = False

        self.load_data()
        self.add_mobs()

    def load_data(self):
        self.load_images()
        self.load_sounds()
        self.load_high_score()

    def load_images(self):
        self.sprite_sheet = self.game.resource_manager.get_image("spritesheet")
        self.background = self.game.resource_manager.get_image("game_screen")
        self.background_rect = self.background.get_rect()

    def load_sounds(self):
        self.high_score_sound = pg.mixer.Sound(
		    self.game.resource_manager.get_sound("high_score_sound"))
        self.high_score_sound.set_volume(0.6)
        # self.enemy_sounds = []
        # for snd in ['fastinvader1.wav','fastinvader2.wav','fastinvader3.wav','fastinvader4.wav']:
        # 	self.enemy_sounds.append(pg.mixer.Sound(snd))
        # self.enemy_sounds[0].set_volume(0.08)
        # self.enemy_sounds[3].set_volume(0.1)

    def load_high_score(self):
        self.game.high_score = load_high_score()
        self.game.orig_high_score = self.game.high_score

    def add_boss(self):
        now = pg.time.get_ticks()
        if now - self.boss_last_update >= self.rand_delay:
            self.boss_last_update = now
            self.rand_delay = random.randrange(4600, 22000)
            if len(self.game.bosses) < 1 and self.game.player1.alive():
                self.game.boss = Boss(self.game)
                self.game.all_sprites.add(self.game.boss)
                self.game.bosses.add(self.game.boss)

		# return(self.p1score)

    def add_mobs(self):
        Bmobs_y_list = [100, 166]
        for ypos in Bmobs_y_list:
            for i in range(10):
                self.game.bigenemy = Mob(((i+1)*70)-15, ypos, "ep", 50,  self.game)
                self.game.all_sprites.add(self.game.bigenemy)
                self.game.Bmobs.add(self.game.bigenemy)
        mob_y_list = [227, 297, 367]
        for ypos in mob_y_list:
            for i in range(10):
                self.newmob(((i+1)*70)-15, ypos)

    def newmob(self, x, y):
        self.game.enemy = Mob(x, y, "samroy", 100,  self.game)
        self.game.all_sprites.add(self.game.enemy)
        self.game.mobs.add(self.game.enemy)

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.game.quit()
            elif event.type == pg.KEYDOWN:
                self._handle_keydown(event)

        self.check_joystick()

    def _handle_keydown(self, event):
        if event.key == pg.K_ESCAPE:
            self.game.quit()
        elif event.key == pg.K_p:  # Pause game
            if self.game.boss is not None:  # Pause the boss sound if boss exists
                self.game.boss.channel.pause()
            self.game.change_state("pause")

    def check_joystick(self):
        try:
            if self.game.joystick1:
                # Joystick 1 check
                if self.game.joystick_handler1.is_button_pressed(8):
                    self.game.quit()
                if self.game.joystick_handler1.is_button_pressed(9):
                    if self.game.boss is not None:  # Pause the boss sound if boss exists
                        self.game.boss.channel.pause()
                    self.game.change_state("pause")

            if self.game.joystick2:
                #joystick 2 check
                if self.game.joystick_handler2.is_button_pressed(6):
                    self.game.quit()
                if self.game.joystick_handler2.is_button_pressed(7):
                    if self.game.boss is not None:  # Pause the boss sound if boss exists
                        self.game.boss.channel.pause()
                    self.game.change_state("pause")

        except AttributeError as e:
            print(f"Joystick error: {e}")

    def update(self):
        self.game.all_sprites.update()

		# Play enemy move sound
		# self.play_mob_movesound()

		# Spawn a boss randomly
        self.add_boss()

		# Check to see if a bullet hit a mob
        if all(item is True for item in self.game.players):
            self.game.enemy_checks.enemy_hit_check(
			    self.game.mobs, 10, self.game.player2_bullets, False)
            self.game.enemy_checks.enemy_hit_check(
			    self.game.Bmobs, 30, self.game.player2_bullets, False)
            self.game.enemy_checks.enemy_hit_check(
			    self.game.bosses, 100, self.game.player2_bullets, True)

        self.game.enemy_checks.enemy_hit_check(self.game.mobs, 10, self.game.player1_bullets, False)
        self.game.enemy_checks.enemy_hit_check(
		    self.game.Bmobs, 30, self.game.player1_bullets, False)
        self.game.enemy_checks.enemy_hit_check(
		    self.game.bosses, 100, self.game.player1_bullets, True)

		# Check if player has killed all the mobs
        if self.game.level_checks.level_check():
            #Check what player are alive and make a list of their x positions
            self.alive_players_xpos = [
                player.rect.centerx for player in self.game.player_group]
 
			# reset all mobs
            self.game.enemy_checks.move_delay = 600
            self.game.enemy_checks.speedx = 5
            self.game.enemy_checks.mob_direction = True
            self.add_mobs()
            #switch to level_change state
            self.game.change_state(
                "level_change", xpos_data=self.alive_players_xpos)

		# Check to see if a mob bullet has hit either player
        if all(item is True for item in self.game.players):
            self.game.player_checks.player_hit_by_bullet(self.game.player2)
        self.game.player_checks.player_hit_by_bullet(self.game.player1)

        if len(self.game.player_group) == 0 and not self.game.player_checks.expl.alive():
            self.game.change_state("gameover")

		# Check to see if a mob has hit either player
        if all(item is True for item in self.game.players):
            self.game.player_checks.player_hit_by_mob(self.game.player2)
        self.game.player_checks.player_hit_by_mob(self.game.player1)

		# Check if enemies have hit the walls and update movement
        now = pg.time.get_ticks()
        if now - self.last_update >= self.game.enemy_checks.move_delay:
            self.last_update = now
			# self.enemy_check()
            self.game.enemy_checks.enemy_direction_check()

		# Update enemy speed
        self.game.enemy_checks.update_enemy_speed()
		# Check for new high score
        meth.new_high_score_check(self.game, self.high_score_sound)

    def draw(self):
        self.game.win.blit(self.background, self.background_rect)
        self.draw_hud()

    def draw_player_score(self, score, x, y):
        meth.draw_text(surf=self.game.win, text=str(score), size=18, x=x, y=y)

    def draw_shields(self, x, y, shield_amm):
        meth.draw_shields(surf=self.game.win, x=x, y=y, shield_amm=shield_amm)

    def draw_high_score(self):
        meth.draw_text(surf=self.game.win, text=str(self.game.high_score),
		               size=18, x=const.SCREENWIDTH/2, y=4)
        
    def draw_lives(self, x, y, player):
        meth.draw_lives(surf=self.game.win, x=x, y=y, player=player)

    def draw_hud(self):
        if all(item is True for item in self.game.players):
            self.draw_player_score(self.game.p2score, x=557, y=6)
            self.draw_shields(x=608, y=8, shield_amm=self.game.player2.shield)
            self.draw_lives(x=720, y=3, player=self.game.player2)

        self.draw_player_score(self.game.p1score, x=112, y=6)
        self.draw_high_score()
        self.draw_shields(x=166, y=8, shield_amm=self.game.player1.shield)
        self.draw_lives(x=278, y=3, player=self.game.player1)
        self.game.all_sprites.draw(self.game.win)
        pg.display.update()

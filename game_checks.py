'''
SAMROIYOD GAME CHECK METHODS developed by Mr Steven J walden
    SEP. 2024
    SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND


[See License.txt file]
'''
import pygame as pg
import constants as const
from random import random, randrange
from sprites import PowerUp, Explosion, Shield1, Shield2


class CheckEnemy:
    def __init__(self, game):
        #In game enemy sprite status and collision checks class
        self.game = game
        self.direction_switch = False
        self.mob_direction = True  # True for right, False for left
        self.move_enemy_y = 12
        self.speedx = 5
        self.move_delay = 600
        self.last_direction_change = pg.time.get_ticks()  # Tracks last change time

    def enemy_direction_check(self):
        # Calculate time since the last direction change
        current_time = pg.time.get_ticks()
        time_since_last_change = current_time - self.last_direction_change

        # Check if any enemy has reached the screen edge
        for enemy in self.game.mobs.sprites() + self.game.Bmobs.sprites():
            if (enemy.rect.centerx >= const.SCREENWIDTH - 25 or enemy.rect.centerx <= 25):
                self.direction_switch = True
                break  # No need to keep checking once the switch is triggered

        # If a direction change is triggered and cooldown period has passed
        if self.direction_switch and time_since_last_change > self.move_delay:
            # Reset flags
            self.direction_switch = False
            self.mob_direction = not self.mob_direction  # Toggle direction

            # Move all enemies down once per switch
            for mob in self.game.mobs.sprites() + self.game.Bmobs.sprites():
                mob.rect.y += self.move_enemy_y

            # Update the last direction change time
            self.last_direction_change = current_time


    def enemy_hit_check(self, enemy, score_amm, bulletlist, check_group_type):
        #Checks to see if a bullet has collided with an enemy
        hits = pg.sprite.groupcollide(enemy, bulletlist, True, True)
        for hit in hits:
            if bulletlist == self.game.player2_bullets:
                self.game.p2score += score_amm
                if self.game.p2score > self.game.high_score: #Update high score
                    self.game.high_score = self.game.p2score
            else:
                self.game.p1score += score_amm
                if self.game.p1score > self.game.high_score: #Update high score
                    self.game.high_score = self.game.p1score

            if check_group_type: #Bool value for checking the right group
                self.game.boss.sound.stop()
                if random() >= 0.7:
                    self.powerup = PowerUp(hit.rect.center, 'boss', self.game)
                    self.game.all_sprites.add(self.powerup)
                    self.game.powerups.add(self.powerup)
                self.expl = Explosion(hit.rect.center, 'boss', 0, self.game, "boss")
            else:
                if random() >= 0.9:
                    self.powerup = PowerUp(hit.rect.center, 'norm', self.game)
                    self.game.all_sprites.add(self.powerup)
                    self.game.powerups.add(self.powerup)
                self.expl = Explosion(hit.rect.center, 'lg', 24, self.game, "mob")
            self.game.all_sprites.add(self.expl)
    
    def update_enemy_speed(self):
        mob_count = len(self.game.mobs.sprites()) + len(self.game.Bmobs.sprites())
        if mob_count <= 4:
            self.move_delay = 30
            self.speedx = 12
            self.move_enemy_y = 50
        elif mob_count <= 8:
            self.move_delay = 80
            self.move_enemy_y = 30
        elif mob_count <= 12:
            self.move_delay = 200
            self.speedx = 9
            self.move_enemy_y = 20
        elif mob_count <= 22:
            self.move_delay = 300
            self.speedx = 7
            self.move_enemy_y = 18
        elif mob_count <= 32:
            self.move_delay = 400
            self.speedx = 6
            self.move_enemy_y = 14


class CheckPlayer:
    def __init__(self, game):
        #In game player sprite status and collision checks class
        self.game = game


    def player_hit_by_mob(self, player):
		#Check to see if a mob has hit the player
        hits = pg.sprite.spritecollide(player, self.game.mobs, True) + pg.sprite.spritecollide(player, self.game.Bmobs, True)
        for hit in hits:
            self.player_death(hit=hit.rect.center, player=player)
            player.shield = 0
            player.lives = 0
            player.hide()
            # if not self.game.expl.alive():
            self.game.playing = False

    def player_hit_by_bullet(self, player):
		#Check to see if a bullet has hit the player
        hits = pg.sprite.spritecollide(player, self.game.mob_bullets, True)
        for hit in hits:
            self.expl = Explosion((hit.rect.x, hit.rect.y), 'sm', 25, self.game, "boss")
            self.game.all_sprites.add(self.expl)
			#activate moving shield if shield powerup is still active
            if player.active_shield == True:
                try:
                    if player == self.game.player2:
                        self.moving_shield2 = Shield2(xpos=player.rect.centerx, game=self.game)
                        self.game.all_sprites.add(self.moving_shield2)
                except AttributeError:
                    pass
                try:
                    if player == self.game.player1:
                        self.moving_shield1 = Shield1(xpos=player.rect.centerx, game=self.game)
                        self.game.all_sprites.add(self.moving_shield1)
                except AttributeError:
                    pass
            else:
                player.shield -= randrange(10,30)
            if player.shield <= 0:
                player.lives -= 1
				#move the player off the screen
                player.hide()

                if player.lives <= 0:
                    self.player_death(hit=hit.rect.center, player=player)
                    player.shield = 100

    def player_death(self, hit, player):
        if len(self.game.player_group) == 2:
            self.expl = Explosion(hit, "boss", 100, self.game, "boss")
            self.game.all_sprites.add(self.expl)
			# check to see if both player are dead
            player.kill()
        else:
            self.expl = Explosion(hit, "boss", 100, self.game, "death")
            self.game.all_sprites.add(self.expl)
			# removes all the bullets after player death
            for bullet in self.game.mob_bullets.sprites():
                bullet.kill()
            self.game.mob_bullets.empty()
            self.game.powerups.empty()
            pg.mixer.music.fadeout(2000)
			# self.enemy_sounds[0].stop()
			# self.enemy_sounds[3].stop()
            if self.game.boss is not None:
                self.game.boss.sound.fadeout(2000)
            player.kill()
        try:
            if player == self.player2:
                self.game.moving_shield2.kill()
        except AttributeError:
            pass
        try:
            if player == self.player1:
                self.game.moving_shield1.kill()
        except AttributeError:
            pass


class CheckLevel:
    def __init__(self, game):
        self.game = game

    def level_check(self):
        #Checks all mobs are killed and removes bullets etc
        if len(self.game.mobs) + len(self.game.Bmobs) <= 0 and not self.game.enemy_checks.expl.alive():
            for bullet in self.game.player1_bullets.sprites():
                bullet.kill()
            self.game.player1_bullets.empty()
            for bullet in self.game.player2_bullets.sprites():
                bullet.kill()
            self.game.player2_bullets.empty()
            for bullet in self.game.mob_bullets.sprites():
                bullet.kill()
            self.game.mob_bullets.empty()
            for powerup in self.game.powerups.sprites():
                powerup.kill()
            self.game.powerups.empty()

            if len(self.game.bosses) > 0:
                self.game.boss.kill()
                self.game.boss.sound.fadeout(1500)

            self.game.game_level += 1
            return True

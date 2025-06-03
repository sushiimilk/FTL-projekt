import pygame
from ui import Button, Cursor
from ship import Ship, EnemyShip
from healthbar import Bar
import random

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/Hangar Background.png"), screen.get_size())
        self.ship_image = pygame.image.load("assets/Kestrel/Kestrel Cruiser closed.png").convert_alpha()
        self.font = pygame.font.Font("assets/C&C Red Alert.ttf", 40)
        self.button = Button(1020, 50, 130, 40, "START", self.font)
        self.cursor = Cursor()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ship_image, (200, -18))
        self.button.draw(self.screen)
        self.cursor.draw(self.screen)

    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN and self.button.is_hovered():
            game.state = "game"



class GameScreen:
    def __init__(self, screen):
        #backgrounds and stuff
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/Backgrounds/bg_darknebula.png"), screen.get_size())
        self.cursor = Cursor()

        self.health = 100
        self.shields = 50

        #player ship
        self.ship = Ship("assets/Kestrel/Kestrel Cruiser open.png", screen.get_width()//2, screen.get_height()//2)
        self.health_bar = Bar(x=40, y=60, width=200, height=24, max_value=100, fill_color=(200, 200, 200), label="HULL")
        self.shield_bar = Bar(x=40, y=110, width=200, height=20, max_value=50, fill_color=(0, 0, 255), label="SHIELDS")

        #Enemy ships and stage:

        self.stage = 1

        self.enemy_ship_paths = [
            "assets/AutoScout/Auto-Scout.png",
            "assets/Mantis/Mantis Fighter.png",
            "assets/RFighter/Rebel Fighter.png"
        ]
        self.boss_ship_path = "assets/RFlagship/Flagship closed.png"
        self.spawn_enemy()

        self.attack_button = Button(520, 600, 160, 40, "ATTACK", pygame.font.Font("assets/C&C Red Alert.ttf", 24))



    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)
        self.cursor.draw(self.screen)

        self.health_bar.update(self.health)
        self.shield_bar.update(self.shields)

        self.health_bar.draw(self.screen)
        self.shield_bar.draw(self.screen)

        #Enemy ships and stuff
        self.enemy.draw(self.screen)
        self.enemy_health_bar.update(self.enemy.health)
        self.enemy_shield_bar.update(self.enemy.shield)
        self.enemy_health_bar.draw(self.screen)
        self.enemy_shield_bar.draw(self.screen)

        self.attack_button.draw(self.screen)


    def spawn_enemy(self):
        if self.stage < 3:
            enemy_image = random.choice(self.enemy_ship_paths)
        else:
            enemy_image = self.boss_ship_path

        self.enemy = EnemyShip(enemy_image, x=900, y=200)

        self.enemy_health_bar = Bar(900, 60, 200, 24,
                                    self.enemy.max_health, (200, 0, 0),
                                    "ENEMY HULL", "assets/C&C Red Alert.ttf")

        self.enemy_shield_bar = Bar(900, 110, 200, 24,
                                    self.enemy.max_shield, (0, 150, 255),
                                    "ENEMY SHIELDS", "assets/C&C Red Alert.ttf")


    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN and self.attack_button.is_hovered():
            #Atakowanie przeciwnika
            self.enemy.take_damage(random.randint(18, 25))
            #Atak od przeciwnika
            if self.shields > 0:
                damage = min(15, self.shields)
                self.shields -= damage
                leftover = 15 - damage
                self.health -= leftover
            else:
                self.health -= 15
            if self.health <= 0:
                print("PRZEGRANA")
                game.state = "loss"

        if self.enemy.health <= 0:
            self.stage += 1
            if self.stage <= 3:
                self.spawn_enemy()
            else:
                print("WYGRANA") #zamienic na ekran koncowy
                game.state = "victory"

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if self.shields > 0:
        #         self.shields -= 10
        #     else:
        #         self.health -= 10
        #
        # pass  # Add later for gameplay input
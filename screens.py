import pygame
from ui import Button, Cursor
from ship import Ship
from healthbar import Bar

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
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/Backgrounds/bg_darknebula.png"), screen.get_size())
        self.ship = Ship("assets/Kestrel/Kestrel Cruiser open.png", screen.get_width()//2, screen.get_height()//2)
        self.cursor = Cursor()

        self.health = 100
        self.shields = 50
        self.health_bar = Bar(x=40, y=60, width=200, height=24, max_value=100, fill_color=(200, 200, 200), label="HULL")
        self.shield_bar = Bar(x=40, y=110, width=200, height=20, max_value=50, fill_color=(0, 0, 255), label="SHIELDS")


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)
        self.cursor.draw(self.screen)

        self.health_bar.update(self.health)
        self.shield_bar.update(self.shields)

        self.health_bar.draw(self.screen)
        self.shield_bar.draw(self.screen)


    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.shields > 0:
                self.shields -= 10
            else:
                self.health -= 10

        pass  # Add later for gameplay input
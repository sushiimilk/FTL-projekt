import pygame, random, time, math
from ui import Button, Cursor
from ship import Ship, EnemyShip
from healthbar import Bar

class MenuScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/Hangar Background.png"),
                                                 screen.get_size())
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and self.button.is_hovered():
            game.state = "intro"



class IntroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/Backgrounds/bg_darknebula.png"),
                                                 screen.get_size())
        self.ship = Ship("assets/Kestrel/Kestrel Cruiser closed.png",
                         screen.get_width() // 2, screen.get_height() // 2)
        self.cursor = Cursor()
        self.font = pygame.font.Font("assets/C&C Red Alert.ttf", 28)

        self.full_text = (
            "Your ship's hyperdrive has failed.\n"
            "You're stranded in hostile space...\n"
            "Steal fuel and fight your way home!\n"
            "You see the first enemy ship approaching..."
        )

        self.typing_start_time = None
        self.text_speed = 30  # characters per second

        self.jump_button = Button(520, 600, 120, 40, "JUMP", self.font)

    def get_typed_text(self):
        if self.typing_start_time is None:
            return ""
        elapsed = time.time() - self.typing_start_time
        chars_to_show = min(int(elapsed * self.text_speed), len(self.full_text))
        return self.full_text[:chars_to_show]

    def start(self):
        if self.typing_start_time is None:
            self.typing_start_time = time.time()

    def draw(self, game):

        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)

        #box behind the intro text
        box_surface = pygame.Surface((700, 200), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 160))
        self.screen.blit(box_surface, (50, 80))

        # intro text
        current_text = self.get_typed_text()
        lines = current_text.split("\n")
        y_offset = 100
        for line in lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (80, y_offset))
            y_offset += 40

        self.jump_button.draw(self.screen)
        self.cursor.draw(self.screen)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

        game.intro_screen.start()
        game.state = "intro"

        if event.type == pygame.MOUSEBUTTONDOWN and self.jump_button.is_hovered():
            game.state = "game"


class GameScreen:
    def __init__(self, screen):
        #backgrounds and stuff
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/Backgrounds/bg_darknebula.png"),
                                                 screen.get_size())
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
        self.cursor.draw(self.screen)


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

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
                game.state = "death"

        if self.enemy.health <= 0:
            self.stage += 1
            if self.stage <= 3:
                self.spawn_enemy()
            else:
                print("WYGRANA") #zamienic na ekran koncowy
                game.state = "victory"

class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/C&C Red Alert.ttf", 50)
        self.smaller_font = pygame.font.Font("assets/C&C Red Alert.ttf", 20)
        self.cursor = Cursor()

        self.quit_button = Button((screen.get_width()//2 - 55), 510, 110, 50, "QUIT", self.font)
        self.menu_button = Button((screen.get_width()//2 - 117), 450, 234, 50, "MAIN MENU", self.font)

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("MISSION FAILED", True, (255, 0, 0))
        small_text = self.smaller_font.render("we'll get 'em next time...", True, (255, 0, 0))
        self.screen.blit(text, ((self.screen.get_width()//2 - text.get_width() // 2),220))
        self.screen.blit(small_text, ((self.screen.get_width() // 2 - small_text.get_width() // 2), 265))
        self.quit_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        self.cursor.draw(self.screen)

    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if self.quit_button.is_hovered():
                    pygame.quit()
                if self.menu_button.is_hovered():
                    game.game_screen = GameScreen(game.screen)
                    game.intro_screen = IntroScreen(game.screen)
                    game.state = "menu"
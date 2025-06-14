import pygame, random, time, math
from ui import *
from ship import *
from healthbar import Bar
from fonts import FONTS
from projectiles import *

class ScreenBase:
    def __init__(self, screen):
        self.screen = screen

class MenuScreen(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.transform.scale(pygame.image.load("assets/Hangar Background.png"),
                                                 screen.get_size())
        self.ship_image = pygame.image.load("assets/Kestrel/Kestrel Cruiser closed.png").convert_alpha()
        self.font = FONTS["large"]
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
                game.running = False
                pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and self.button.is_hovered():
            game.state = "intro"



class IntroScreen(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.background = pygame.transform.scale(pygame.image.load("assets/Backgrounds/bg_darknebula.png"),
                                                 screen.get_size())
        self.ship = Ship("assets/Kestrel/Kestrel Cruiser closed.png",
                         screen.get_width() // 2, screen.get_height() // 2)
        self.cursor = Cursor()
        self.font = FONTS["medium"]

        self.full_text = (
            "Your ship's hyperdrive has failed.\n"
            "You're stranded in hostile space...\n"
            "Steal fuel and fight your way home!\n"
            "You see the first enemy ship approaching..."
        )

        self.typing_start_time = None
        self.text_speed = 30  # characters per second

        self.jump_button = Button(screen.get_width()//2-37.5, 600, 95, 40, "JUMP", self.font)

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
        self.ship.draw(self.screen, centered=True)

        #box behind the intro text
        box_surface = pygame.Surface((700, 200), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 160))
        self.screen.blit(box_surface, (self.screen.get_width() // 2 - 350, 80))

        # intro text
        current_text = self.get_typed_text()
        lines = current_text.split("\n")
        y_offset = 100
        for line in lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(centerx=self.screen.get_width() // 2)
            text_rect.top = y_offset
            self.screen.blit(text_surf, text_rect)
            y_offset += 40

        self.jump_button.draw(self.screen)
        self.cursor.draw(self.screen)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game.running = False
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.jump_button.is_hovered():
                game.state = "game"
                game.game_screen.last_enemy_attack = time.time() # ---LOGIKA ZEBY PRZECIWNIK POCZEKAL Z ATAKIEM
        self.start()


class GameScreen(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        #backgrounds and stuff

        self.background_paths = [
            "assets/Backgrounds/bg_darknebula.png",
            "assets/Backgrounds/bg_blueStarcluster.png",
            "assets/Backgrounds/bg_lonelyRedStar.png",
            "assets/Backgrounds/bg_lonelystar.png",
            "assets/Backgrounds/low_pulsar.png",
            "assets/Backgrounds/low_sun.png",
            "assets/Backgrounds/low_nebula.png",
        ]
        self.boss_background = "assets/Backgrounds/bg_final.png"
        self.last_background = None

        self.cursor = Cursor()

        #player ship
        self.ship = Ship("assets/Kestrel/Kestrel Cruiser closed.png", screen.get_width()//2, screen.get_height()//2)
        self.engine_image = pygame.image.load("assets/Kestrel/Kestrel Engine.png").convert_alpha()
        self.engine_image = pygame.transform.rotate(self.engine_image, 90)  # obrót o 90 stopni w lewo
        self.ship.move(-300, 35)
        self.health_bar = Bar(x=40, y=60, width=200, height=24, max_value=100, fill_color=(200, 200, 200), label="HULL")
        self.shield_bar = Bar(x=40, y=110, width=200, height=20, max_value=50, fill_color=(0, 0, 255), label="SHIELDS")

        # ---BRONIE---
        self.laser_ready_img = pygame.image.load("assets/Kestrel/Laser ready.png").convert_alpha()
        self.laser_unready_img = pygame.image.load("assets/Kestrel/Laser unready.png").convert_alpha()
        self.rocket_ready_img = pygame.image.load("assets/Kestrel/Rocket ready.png").convert_alpha()
        self.rocket_unready_img = pygame.image.load("assets/Kestrel/Rocket unready.png").convert_alpha()

        #Atak gracza (cooldowny)
        self.laser_attack_cooldown = 1.5        #cooldown lasera (sekundy)
        self.rocket_attack_cooldown = 4.0       #cooldown rakiety 
        self.enemy_attack_cooldown = 2.0        #cooldown ataku przeciwnika
        self.last_player_laser_attack = 0      # czas ostatniego ataku laserem
        self.last_player_rocket_attack = 0     # czas ostatniego ataku rakietą

        #Enemy ships and stage:

        self.stage = 1

        #przerwy miedzy przeciwnikami
        self.waiting_for_jump = False
        self.jump_button = Button(screen.get_width()//2-47.5, 50, 95, 40, "JUMP", FONTS["medium"])

        self.enemy_ship_paths = [
            "assets/AutoScout/Auto-Scout.png",
            "assets/Mantis/Mantis Fighter.png",
            "assets/RFighter/Rebel Fighter.png",
            "assets/Lanius/Lanius.png",
            "assets/EFighter/Energy Fighter.png"
        ]
        random.shuffle(self.enemy_ship_paths) 

        
        self.boss_ship_path = "assets/RFlagship/Flagship closed.png"
        self.spawn_enemy()


        #attak gracza
        self.laser_button = Button(screen.get_width()//2-59, 600, 118, 40, "LASER", FONTS["medium"])
        self.rocket_button= Button(screen.get_width()//2-59, 650, 118, 40, "ROCKET", FONTS["medium"])

        # ---PROJECTILES---
        self.laser_projectiles = []
        self.rocket_projectiles = []

    def enemy_attack(self, game):
        now = time.time()
        #atak przeciwnika
        if now - self.last_enemy_attack >= self.enemy_attack_cooldown:
            # atak przeciwnika
            self.last_enemy_attack = now
            self.ship.take_damage(random.randint(10,15))
            if self.ship.health <= 0:
                game.state = "death"

    def spawn_enemy(self):
        #zmiana tła
        if self.stage < 5:
            available_backgrounds = [bg for bg in self.background_paths if bg != self.last_background]
            chosen_bg = random.choice(available_backgrounds)
            self.last_background = chosen_bg
        else:
            chosen_bg = self.boss_background

        self.background = pygame.transform.scale(
            pygame.image.load(chosen_bg),
            self.screen.get_size()
        )

        #Losowanie przeciwnika
        if self.stage < 5:
            if self.enemy_ship_paths:
                enemy_image = self.enemy_ship_paths.pop()
        else:
            enemy_image = self.boss_ship_path

        #Rysowanie przeciwnika
        self.enemy = EnemyShip(enemy_image, x=900, y=200)
        self.enemy.move(0, 200)

        #Tarcze i hp przeciwnika
        self.enemy_health_bar = Bar(900, 60, 200, 24,
                                    self.enemy.max_health, (200, 0, 0),
                                    "ENEMY HULL")

        self.enemy_shield_bar = Bar(900, 110, 200, 24,
                                    self.enemy.max_shield, (0, 150, 255),
                                    "ENEMY SHIELDS")
        
        # Ustawienie czasu ostatniego ataku przeciwnika na teraz, aby wymusić cooldown na starcie rundy
        self.last_enemy_attack = time.time()
        self.enemy_attack_cooldown = 2.0  # lub inna wartość, jeśli chcesz mieć różne cooldowny

    def is_laser_ready(self):
        return (time.time() - self.last_player_laser_attack) >= self.laser_attack_cooldown

    def is_rocket_ready(self):
        return (time.time() - self.last_player_rocket_attack) >= self.rocket_attack_cooldown

    def draw_enemy(self):
        self.enemy.draw(self.screen)
        self.enemy_health_bar.update(self.enemy.health)
        self.enemy_shield_bar.update(self.enemy.shield)
        self.enemy_health_bar.draw(self.screen)
        self.enemy_shield_bar.draw(self.screen)

    def draw(self, game):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen, centered=self.waiting_for_jump)

        # STAGE 1,2,3,etc. 
        font = FONTS["large"]
        stage_text = font.render(f"STAGE {self.stage}", True, (255, 255, 0))
        self.screen.blit(stage_text, (self.screen.get_width() // 2 - stage_text.get_width() // 2, 10))

        #animacja silnikow
        t = time.time()
        #alpha silnikow w zależności od czasu
        #100 to minimalna przezroczystosc, 255 to maksymalna
        #135 to amplituda, 0.5 to przesuniecie fazowe
        #1 Hz to czstotliwosc, czyli 1 pelny cykl na sekundee
        engine_alpha = int(100 + 135 * (0.5 + 0.5 * math.sin(2 * math.pi * t * 1)))

        engine_image = self.engine_image.copy()
        engine_image.set_alpha(engine_alpha)

        # ---POZYCJE BRONI---
        laser_pos = (390, 328)
        rocket_pos = (390, 428)

        if not self.waiting_for_jump:
            if self.is_laser_ready():
                self.screen.blit(self.laser_ready_img, laser_pos)
            else:
                self.screen.blit(self.laser_unready_img, laser_pos)

            if self.is_rocket_ready():
                self.screen.blit(self.rocket_ready_img, rocket_pos)
            else:
                self.screen.blit(self.rocket_unready_img, rocket_pos)

        if not self.waiting_for_jump and self.enemy.health > 0:
            #1 silnik gora
            x = 114
            y = 274
            self.screen.blit(engine_image, (x, y))
            #2 silnik gora
            x = 114
            y = 263
            self.screen.blit(engine_image, (x, y))
            #3 silnik gora
            x = 114
            y = 292
            self.screen.blit(engine_image, (x, y))
            #1 silnik dol
            x = 114
            y = 449 + 14
            self.screen.blit(engine_image, (x, y))
            #2 silnik dol
            x = 114
            y = 449
            self.screen.blit(engine_image, (x, y))
            #3 silnik dol
            x = 114
            y = 449 + 28
            self.screen.blit(engine_image, (x, y))


        self.health_bar.update(self.ship.health)
        self.shield_bar.update(self.ship.shield)

        self.health_bar.draw(self.screen)
        self.shield_bar.draw(self.screen)

        #Enemy ship and bars
        if not self.waiting_for_jump and self.enemy.health > 0:
            self.draw_enemy()

        #auto atak przeciwnika
        if not self.waiting_for_jump and self.enemy.health > 0:
            self.enemy_attack(game)

        if self.enemy.health <= 0 and not self.waiting_for_jump:
            self.waiting_for_jump = True
            self.ship.shield = self.ship.max_shield

        if self.waiting_for_jump:
            self.jump_button.draw(self.screen)
        else:
            # Sprawdź cooldowny
            now = time.time()
            laser_color = (0, 200, 0) if self.is_laser_ready() else (200, 0, 0)   # zielony lub czerwony
            rocket_color = (0, 200, 0) if self.is_rocket_ready() else (200, 0, 0) # zielony lub czerwony

            self.laser_button.draw(self.screen, color=laser_color) #przycisk laseru
            self.rocket_button.draw(self.screen, color=rocket_color) #przycisk rakiety

        # ---PROJECTILES UPDATE, COLLISION & DRAW---
        # Laser projectiles
        for projectile in self.laser_projectiles:
            projectile.update()
            # Initialize tracking attributes if not present
            if not hasattr(projectile, "collision_detected"):
                projectile.collision_detected = False
                projectile.collision_point = None
                projectile.required_depth = None

            if self.enemy.health > 0:
                if not projectile.collision_detected:
                    if projectile.rect.colliderect(self.enemy.rect):
                        projectile.collision_detected = True
                        projectile.collision_point = projectile.rect.center
                        # Set required depth as a fraction of enemy image width (e.g., 40%)
                        enemy_width = self.enemy.rect.width
                        projectile.required_depth = int(enemy_width * 0.5)
                else:
                    # Calculate distance from collision point
                    dx = projectile.rect.centerx - projectile.collision_point[0]
                    dy = projectile.rect.centery - projectile.collision_point[1]
                    distance_after_collision = (dx ** 2 + dy ** 2) ** 0.5
                    if projectile.required_depth is not None and distance_after_collision >= projectile.required_depth + random.randint(-10,20):
                        self.enemy.take_damage(projectile.damage)
                        projectile.active = False
            projectile.draw(self.screen)
        self.laser_projectiles = [p for p in self.laser_projectiles if p.active]

        # Rocket projectiles
        for projectile in self.rocket_projectiles:
            projectile.update()
            if not hasattr(projectile, "collision_detected"):
                projectile.collision_detected = False
                projectile.collision_point = None
                projectile.required_depth = None

            if self.enemy.health > 0:
                if not projectile.collision_detected:
                    if projectile.rect.colliderect(self.enemy.rect):
                        projectile.collision_detected = True
                        projectile.collision_point = projectile.rect.center
                        enemy_width = self.enemy.rect.width
                        projectile.required_depth = int(enemy_width * 0.4)
                else:
                    dx = projectile.rect.centerx - projectile.collision_point[0]
                    dy = projectile.rect.centery - projectile.collision_point[1]
                    distance_after_collision = (dx ** 2 + dy ** 2) ** 0.5
                    if projectile.required_depth is not None and distance_after_collision >= projectile.required_depth:
                        self.enemy.take_damage(projectile.damage)
                        projectile.active = False
            projectile.draw(self.screen)
        self.rocket_projectiles = [p for p in self.rocket_projectiles if p.active]

        # Remove all projectiles if waiting for jump
        if self.waiting_for_jump:
            self.laser_projectiles.clear()
            self.rocket_projectiles.clear()

        self.cursor.draw(self.screen)

    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
                pygame.quit()

        # ---LASER SHOOTING---
        if event.type == pygame.MOUSEBUTTONDOWN and self.laser_button.is_hovered():
            now = time.time()
            if self.is_laser_ready():
                self.last_player_laser_attack = time.time()
                # Spawn laser projectile (with damage)
                laser_gun_x = 390+30
                laser_gun_y = 328+5
                dx = 1  # rightwards
                dy = 0
                self.laser_projectiles.append(
                    LaserProjectile(laser_gun_x, laser_gun_y, dx, dy, "assets/Projectiles/laser projectile.png", damage=random.randint(18, 25))
                )
        # ---ROCKET SHOOTING---
        if event.type == pygame.MOUSEBUTTONDOWN and self.rocket_button.is_hovered():
            now = time.time()
            if self.is_rocket_ready():
                self.last_player_rocket_attack = time.time()
                # Spawn rocket projectile (with damage)
                rocket_gun_x = 390+40
                rocket_gun_y = 428+15
                dx = 1
                dy = 0
                self.rocket_projectiles.append(
                    RocketProjectile(rocket_gun_x, rocket_gun_y, dx, dy, "assets/Projectiles/missile.png", damage=random.randint(24, 35))
                )

        if event.type == pygame.MOUSEBUTTONDOWN and self.jump_button.is_hovered() and self.waiting_for_jump:
            self.stage += 1
            if self.stage <= 5:
                self.spawn_enemy()
                self.waiting_for_jump = False
            else:
                game.state = "victory"



class GameOver(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = FONTS["huge"]
        self.smaller_font = FONTS["small"]
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
                    game.running = False
                    pygame.quit()
                    return
                if self.menu_button.is_hovered():
                    game.game_screen = GameScreen(game.screen)
                    game.intro_screen = IntroScreen(game.screen)
                    game.state = "menu"

class Victory(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = FONTS["huge"]
        self.smaller_font = FONTS["small"]
        self.cursor = Cursor()
        self.quit_button = Button((screen.get_width() // 2 - 55), 510, 110, 50, "QUIT", self.font)
        self.menu_button = Button((screen.get_width() // 2 - 117), 450, 234, 50, "MAIN MENU", self.font)

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("MISSION SUCCESS", True, (0, 255, 0))
        small_text = self.smaller_font.render("you made it back home!", True, (0, 255, 0))
        self.screen.blit(text, ((self.screen.get_width() // 2 - text.get_width() // 2), 220))
        self.screen.blit(small_text, ((self.screen.get_width() // 2 - small_text.get_width() // 2), 265))
        self.quit_button.draw(self.screen)
        self.menu_button.draw(self.screen)
        self.cursor.draw(self.screen)

    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit_button.is_hovered():
                game.running = False
                pygame.quit()
                return
            if self.menu_button.is_hovered():
                game.game_screen = GameScreen(game.screen)
                game.intro_screen = IntroScreen(game.screen)
                game.state = "menu"
import random, math
from ui import *
from ship import *
from healthbar import Bar
from fonts import FONTS
from projectiles import *

class ScreenBase:
    def __init__(self, screen):
        self.screen = screen

    @staticmethod
    # handle_quit_menu_buttons in ScreenBase is a @staticmethod because it
    # does not use or modify any instance (self) or class (cls) attributes.
    # It only processes the event and buttons passed as arguments.
    # Making it static clarifies that it does not depend on the state of a ScreenBase object.
    def handle_quit_menu_buttons(event, game, quit_button, menu_button):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.is_hovered():
                game.running = False
                return True
            if menu_button.is_hovered():
                game.game_screen = GameScreen(game.screen)
                game.intro_screen = IntroScreen(game.screen)
                game.state = "menu"
                return True
        return False

    def draw_quit_menu_buttons(self, text, small_text, quit_button, menu_button, cursor):
        self.screen.blit(text, ((self.screen.get_width() // 2 - text.get_width() // 2), 220))
        self.screen.blit(small_text, ((self.screen.get_width() // 2 - small_text.get_width() // 2), 265))
        quit_button.draw(self.screen)
        menu_button.draw(self.screen)
        cursor.draw(self.screen)

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
                return

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

    def draw(self):
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
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.jump_button.is_hovered():
                game.state = "game"
                game.start_time = time.time() # do statów
                game.game_screen.last_enemy_attack = time.time() # ---LOGIKA ZEBY PRZECIWNIK POCZEKAL Z ATAKIEM
        self.start()


class Explosion:
    def __init__(self, pos, sprite_path, frame_size=(512, 512), frame_count=64, frame_duration=0.01):
        self.frames = []
        self.load_frames(sprite_path, frame_size, frame_count)
        self.index = 0
        self.frame_duration = frame_duration
        self.timer = 0
        self.pos = (pos[0] - frame_size[0] // 2, pos[1] - frame_size[1] // 2)
        self.finished = False

    def load_frames(self, sprite_path, frame_size, frame_count):
        sheet = pygame.image.load(sprite_path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frames_per_row = sheet_width // frame_size[0]
        for i in range(frame_count):
            row = i // frames_per_row
            col = i % frames_per_row
            x = col * frame_size[0]
            y = row * frame_size[1]
            frame = sheet.subsurface((x, y, frame_size[0], frame_size[1]))
            self.frames.append(frame)

    def update(self, dt):
        if self.finished:
            return
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.finished = True

    def draw(self, surface):
        if not self.finished and self.index < len(self.frames):
            surface.blit(self.frames[self.index], self.pos)


class GameScreen(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.cursor = Cursor()
        self.stage = 1
        self.waiting_for_jump = False
        self.enemy_destroyed_explosion_played = False

        # --Sound Effects--
        self.sfx_laser = pygame.mixer.Sound("assets/sound/laser.wav")
        self.sfx_explosion = pygame.mixer.Sound("assets/sound/rocket_explosion.wav")
        self.sfx_player_hit = pygame.mixer.Sound("assets/sound/player_damage.wav")
        self.sfx_laser.set_volume(0.6)
        self.sfx_explosion.set_volume(0.3)
        self.sfx_player_hit.set_volume(0.5)

        # --Backgrounds--
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
        self.background = None

        # --Player Ship--
        self.ship = Ship("assets/Kestrel/Kestrel Cruiser closed.png", screen.get_width()//2, screen.get_height()//2)
        self.ship.move(-300, 35)
        self.player_destroyed_explosion_played = False

        # --Engine Animation--
        self.engine_image = pygame.image.load("assets/Kestrel/Kestrel Engine.png").convert_alpha()

        # --Paski HP/Shield--
        self.health_bar = Bar(x=40, y=60, width=200, height=24, max_value=100, fill_color=(200, 200, 200), label="HULL")
        self.shield_bar = Bar(x=40, y=110, width=200, height=20, max_value=50, fill_color=(0, 0, 255), label="SHIELDS")

        # --Guziki--
        self.jump_button = Button(screen.get_width() // 2 - 47.5, 50, 95, 40, "JUMP", FONTS["medium"])
        self.laser_button = Button(screen.get_width() // 2 - 59, 600, 118, 40, "LASER", FONTS["medium"])
        self.rocket_button = Button(screen.get_width() // 2 - 59, 650, 118, 40, "ROCKET", FONTS["medium"])

        # --Bronie--
        self.laser_ready_img = pygame.image.load("assets/Kestrel/Laser ready.png").convert_alpha()
        self.laser_unready_img = pygame.image.load("assets/Kestrel/Laser unready.png").convert_alpha()
        self.rocket_ready_img = pygame.image.load("assets/Kestrel/Rocket ready.png").convert_alpha()
        self.rocket_unready_img = pygame.image.load("assets/Kestrel/Rocket unready.png").convert_alpha()

        # --Cooldowny--
        self.laser_attack_cooldown = 1.5        #cooldown lasera (sekundy)
        self.rocket_attack_cooldown = 4.0       #cooldown rakiety
        self.last_player_laser_attack = 0      # czas ostatniego ataku laserem
        self.last_player_rocket_attack = 0     # czas ostatniego ataku rakietą
        self.last_enemy_attack = 0

        # --Przeciwnicy--
        self.enemy_ship_paths = [
            "assets/AutoScout/Auto-Scout.png",
            "assets/Mantis/Mantis Fighter.png",
            "assets/RFighter/Rebel Fighter.png",
            "assets/Lanius/Lanius.png",
            "assets/EFighter/Energy Fighter.png"
        ]
        random.shuffle(self.enemy_ship_paths)
        self.boss_ship_path = "assets/RFlagship/Flagship closed.png"
        self.enemy_variants = None
        self.enemy = None
        self.enemy_health_bar = None
        self.enemy_shield_bar = None
        self.spawn_enemy()

        # --Pociski i wybuchy--
        self.laser_projectiles = []
        self.enemy_projectiles = []
        self.rocket_projectiles = []
        self.explosions = []

    def is_laser_ready(self):
        return time.time() - self.last_player_laser_attack >= self.laser_attack_cooldown

    def is_rocket_ready(self):
        return time.time() - self.last_player_rocket_attack >= self.rocket_attack_cooldown

    def draw(self, game):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen, centered=self.waiting_for_jump)
        self.draw_stage_label()
        self.draw_engine_animation()
        self.draw_weapons()
        self.health_bar.update(self.ship.health)
        self.shield_bar.update(self.ship.shield)
        self.health_bar.draw(self.screen)
        self.shield_bar.draw(self.screen)
        self.draw_projectiles()
        self.draw_enemy()
        self.enemy_attack()
        self.spawn_enemy_explosion()
        self.draw_jump_button_or_weapons()
        self.update_projectile_collisions(game)
        self.draw_explosions()
        self.cleanup_after_explosions(game)
        self.cursor.draw(self.screen)

    def draw_stage_label(self):
        # STAGE 1,2,3,etc.
        font = FONTS["large"]
        stage_text = font.render(f"STAGE {self.stage}", True, (255, 255, 0))
        self.screen.blit(stage_text, (self.screen.get_width() // 2 - stage_text.get_width() // 2, 10))

    def draw_weapons(self):
        if self.waiting_for_jump:
            return
        laser_pos = (390, 328)
        rocket_pos = (390, 428)
        self.screen.blit(self.laser_ready_img if self.is_laser_ready() else self.laser_unready_img, laser_pos)
        self.screen.blit(self.rocket_ready_img if self.is_rocket_ready() else self.rocket_unready_img, rocket_pos)

    def draw_engine_animation(self):
        if self.waiting_for_jump or self.enemy.health <= 0:
            return
        # alpha silnikow w zależności od czasu
        # 100 to minimalna przezroczystosc, 255 to maksymalna
        # 135 to amplituda, 0.5 to przesuniecie fazowe
        # 1 Hz to czestotliwosc, czyli 1 pelny cykl na sekunde
        alpha = int(100 + 135 * (0.5 + 0.5 * math.sin(2 * math.pi * time.time())))
        image = self.engine_image.copy()
        image.set_alpha(alpha)
        positions = [(114, y) for y in [274, 263, 292, 463, 449, 477]]
        for pos in positions:
            self.screen.blit(image, pos)

    def draw_enemy(self):
        if self.enemy.health > 0:
            self.enemy.draw(self.screen)
            self.enemy_health_bar.update(self.enemy.health)
            self.enemy_shield_bar.update(self.enemy.shield)
            self.enemy_health_bar.draw(self.screen)
            self.enemy_shield_bar.draw(self.screen)
            variant_key = [k for k, v in self.enemy_variants.items() if v == self.enemy.variant][0]
            variant_text = FONTS["small"].render(f"{variant_key.upper()} ENEMY", True, (255, 255, 255))
            self.screen.blit(variant_text, (self.screen.get_width() // 2 - variant_text.get_width() // 2, 50))

    def enemy_attack(self):
        if not self.waiting_for_jump and self.enemy.health > 0 and self.ship.health > 0:
            if time.time() - self.last_enemy_attack >= self.enemy.attack_cooldown:
                self.last_enemy_attack = time.time()
                damage_range = self.enemy.variant["damage"]
                damage = random.randint(*damage_range)
                projectile = LaserProjectile(
                    x=self.enemy.rect.left+30,
                    y=self.enemy.rect.centery,
                    dx=-1,
                    dy=0,
                    image_path="assets/Projectiles/enemy laser.png",
                    damage=damage
                )
                self.enemy_projectiles.append(projectile)

    def draw_jump_button_or_weapons(self):
        if self.waiting_for_jump:
            self.jump_button.draw(self.screen)
        else:
            self.laser_button.draw(self.screen, color=(0, 200, 0) if self.is_laser_ready() else (200, 0, 0))
            self.rocket_button.draw(self.screen, color=(0, 200, 0) if self.is_rocket_ready() else (200, 0, 0))

    def spawn_enemy_explosion(self):
        if self.enemy.health <= 0 and not self.enemy_destroyed_explosion_played:
            self.explosions.append(
                Explosion(
                    self.enemy.rect.center,
                    sprite_path="assets/explosions/explosion 4.png",
                    frame_size=(512, 512),
                    frame_count=64
                )
            )
            self.enemy_destroyed_explosion_played = True

    def cleanup_after_explosions(self, game):
        if self.ship.health <= 0 and self.player_destroyed_explosion_played and not self.explosions:
            game.state = "death"
        if self.enemy.health <= 0 and self.enemy_destroyed_explosion_played and not self.explosions:
            self.waiting_for_jump = True
        if self.waiting_for_jump:
            self.laser_projectiles.clear()
            self.rocket_projectiles.clear()
            self.sfx_explosion.stop()
            self.sfx_laser.stop()
            self.sfx_player_hit.stop()

    def draw_projectiles(self):
        for projectile in self.enemy_projectiles:
            projectile.update()
            projectile.draw(self.screen)
            if projectile.rect.colliderect(self.ship.rect):
                self.ship.take_damage(projectile.damage)
                self.sfx_player_hit.play()
                projectile.active = False

        if self.ship.health <= 0 and not self.player_destroyed_explosion_played:
            self.sfx_explosion.play()
            self.explosions.append(
                Explosion(
                    self.ship.rect.center,
                    sprite_path="assets/explosions/explosion 4.png",
                    frame_size=(512, 512),
                    frame_count=64
                )
            )
            self.player_destroyed_explosion_played = True

        self.enemy_projectiles = [p for p in self.enemy_projectiles if p.active]

    def draw_explosions(self):
        dt = 1 / 60
        for explosion in self.explosions:
            explosion.update(dt)
            explosion.draw(self.screen)
        self.explosions = [e for e in self.explosions if not e.finished]

    def spawn_enemy(self):
        #zmiana tła
        if self.stage < 5:
            available_backgrounds = [bg for bg in self.background_paths if bg != self.background]
            chosen_bg = random.choice(available_backgrounds)
            self.background = chosen_bg
        else:
            chosen_bg = self.boss_background

        self.background = pygame.transform.scale(
            pygame.image.load(chosen_bg),
            self.screen.get_size()
        )

        # --Wariancje--
        self.enemy_variants = {
            "fast": {"hp": 80, "shield": 30, "damage": (8, 15), "cooldown": 1},
            "standard": {"hp": 100, "shield": 50, "damage": (10, 15), "cooldown": 2.0},
            "heavy": {"hp": 175, "shield": 75, "damage": (17, 24), "cooldown": 2.7},
            "shielded": {"hp": 90, "shield": 125, "damage": (10, 15), "cooldown": 2.0},
            "superheavy": {"hp": 250, "shield": 150, "damage": (17, 30), "cooldown": 3.5}
        }

        #Losowanie przeciwnika
        if self.stage < 5 and self.enemy_ship_paths:
            enemy_image = self.enemy_ship_paths.pop()
            variant_key = random.choice(list(self.enemy_variants.keys() - {"superheavy"}))  # Exclude boss class
        else:
            enemy_image = self.boss_ship_path
            variant_key = "superheavy"

        variant = self.enemy_variants[variant_key]

        #Rysowanie przeciwnika
        self.enemy = EnemyShip(enemy_image, x=900, y=200,
                               max_health=variant["hp"],
                               max_shield=variant["shield"])
        self.enemy.variant = variant
        self.enemy.attack_cooldown = variant["cooldown"]
        self.enemy.move(0, 200)

        #Tarcze i hp przeciwnika
        self.enemy_health_bar = Bar(900, 60, 200, 24, self.enemy.max_health, (200, 0, 0), "ENEMY HULL")
        self.enemy_shield_bar = Bar(900, 110, 200, 24, self.enemy.max_shield, (0, 150, 255), "ENEMY SHIELDS")
        self.last_enemy_attack = time.time()
        self.enemy_destroyed_explosion_played = False

    def handle_event(self, event, game):
        if self.ship.health <= 0:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game.running = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.laser_button.is_hovered() and self.is_laser_ready():
                self.sfx_laser.play()
                self.last_player_laser_attack = time.time()
                self.laser_projectiles.append(
                    LaserProjectile(420, 333, 1, 0, "assets/Projectiles/laser projectile.png", random.randint(20, 26))
                )

            if self.rocket_button.is_hovered() and self.is_rocket_ready():
                self.last_player_rocket_attack = time.time()
                self.rocket_projectiles.append(
                    RocketProjectile(430, 443, 1, 0, "assets/Projectiles/missile.png", random.randint(26, 39))
                )

            if self.jump_button.is_hovered() and self.waiting_for_jump:
                self.stage += 1
                if self.stage <= 5:
                    self.spawn_enemy()
                    self.waiting_for_jump = False
                    self.ship.shield = self.ship.max_shield
                else:
                    game.victory_time = int(time.time() - game.start_time)
                    game.state = "victory"

    def update_projectile_collisions(self, game):
        def process_projectile(proj_list, is_rocket):
            for projectile in proj_list:
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
                            projectile.required_depth = int(enemy_width * 0.2) + random.randint(-10, 100)
                    else:
                        dx = projectile.rect.centerx - projectile.collision_point[0]
                        dy = projectile.rect.centery - projectile.collision_point[1]
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        if projectile.required_depth and distance >= projectile.required_depth:
                            self.enemy.take_damage(projectile.damage)
                            game.total_damage_dealt += projectile.damage
                            self.sfx_explosion.play()
                            projectile.active = False
                            explosion_img = "assets/explosions/explosion 2h.png" if is_rocket else "assets/explosions/explosion 1h.png"
                            offset_x = 90 if is_rocket else 0
                            self.explosions.append(
                                Explosion(
                                    (projectile.rect.centerx + offset_x, projectile.rect.centery),
                                    sprite_path=explosion_img,
                                    frame_size=(256, 256),
                                    frame_count=64,
                                )
                            )
                projectile.draw(self.screen)

        process_projectile(self.laser_projectiles, is_rocket=False)
        process_projectile(self.rocket_projectiles, is_rocket=True)

        self.laser_projectiles = [p for p in self.laser_projectiles if p.active]
        self.rocket_projectiles = [p for p in self.rocket_projectiles if p.active]

class GameOver(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = FONTS["huge"]
        self.smaller_font = FONTS["small"]
        self.cursor = Cursor()
        self.quit_button = Button((screen.get_width()//2 - 55), 510, 110, 50, "QUIT", self.font)
        self.menu_button = Button((screen.get_width()//2 - 117), 450, 234, 50, "MAIN MENU", self.font)

    def draw(self):
        if not pygame.display.get_init():
            return
        self.screen.fill((0, 0, 0))
        text = self.font.render("MISSION FAILED", True, (255, 0, 0))
        small_text = self.smaller_font.render("we'll get 'em next time...", True, (255, 0, 0))
        self.draw_quit_menu_buttons(text, small_text, self.quit_button, self.menu_button, self.cursor)

    def handle_event(self, event, game):
        if self.handle_quit_menu_buttons(event, game, self.quit_button, self.menu_button):
            return

class Victory(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.font = FONTS["huge"]
        self.smaller_font = FONTS["small"]
        self.cursor = Cursor()
        self.quit_button = Button((screen.get_width() // 2 - 55), 510, 110, 50, "QUIT", self.font)
        self.menu_button = Button((screen.get_width() // 2 - 117), 450, 234, 50, "MAIN MENU", self.font)

    def draw(self, game):
        if not pygame.display.get_init():
            return
        self.screen.fill((0, 0, 0))
        text = self.font.render("MISSION SUCCESS", True, (0, 255, 0))
        small_text = self.smaller_font.render("you made it back home!", True, (0, 255, 0))
        self.draw_quit_menu_buttons(text, small_text, self.quit_button, self.menu_button, self.cursor)

        duration = game.victory_time if game.victory_time is not None else 0
        damage = game.total_damage_dealt
        summary_text = f"Time: {duration} seconds | Damage Dealt: {damage}"
        summary_surf = self.smaller_font.render(summary_text, True, (255, 255, 255))
        self.screen.blit(summary_surf, (
            self.screen.get_width() // 2 - summary_surf.get_width() // 2, 320))

    def handle_event(self, event, game):
        if self.handle_quit_menu_buttons(event, game, self.quit_button, self.menu_button):
            return
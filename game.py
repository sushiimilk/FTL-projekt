import pygame
from screens import MenuScreen, GameScreen, IntroScreen, GameOver, Victory

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.current_music = None

        # --Stat tracking--
        self.total_damage_dealt = 0
        self.start_time = None
        self.victory_time = None

        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("FTL Clone")
        self.clock = pygame.time.Clock()
        self.state = "menu" #menu, intro, game
        self.running = True

        self.menu_screen = MenuScreen(self.screen)
        self.game_screen = GameScreen(self.screen)
        self.intro_screen = IntroScreen(self.screen)
        self.game_over_screen = GameOver(self.screen)
        self.victory_screen = Victory(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    match self.state:
                        case "menu":
                            self.menu_screen.handle_event(event, self)
                        case "game":
                            self.game_screen.handle_event(event, self)
                        case "intro":
                            self.intro_screen.handle_event(event, self)
                        case "death":
                            self.game_over_screen.handle_event(event, self)
                        case "victory":
                            self.victory_screen.handle_event(event, self)

            # --- MUZYKA ---
            match self.state:
                case "menu":
                    if self.current_music != "menu":
                        pygame.mixer.music.load("assets/sound/menu theme.mp3")
                        pygame.mixer.music.set_volume(0.4)
                        pygame.mixer.music.play(-1)
                        self.current_music = "menu"

                case "intro" | "game":
                    if self.current_music != "game":
                        pygame.mixer.music.load("assets/sound/game theme.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        self.current_music = "game"

                # case "death":
                #     if self.current_music != "death":
                #         pygame.mixer.music.load("assets/sound/gameover_theme.wav")
                #         pygame.mixer.music.set_volume(0.5)
                #         pygame.mixer.music.play(-1)
                #         self.current_music = "death"
                #
                # case "victory":
                #     if self.current_music != "victory":
                #         pygame.mixer.music.load("assets/sound/victory_theme.wav")
                #         pygame.mixer.music.set_volume(0.5)
                #         pygame.mixer.music.play(-1)
                #         self.current_music = "victory"

            # ✅ DRAWING SCREENS
            match self.state:
                case "menu":
                    self.menu_screen.draw()
                case "intro":
                    self.intro_screen.draw()
                case "game":
                    self.game_screen.draw(self)
                case "death":
                    self.game_over_screen.draw()
                case "victory":
                    self.victory_screen.draw(self)

            pygame.display.flip()
            self.clock.tick(60)

        if pygame.get_init():
            pygame.quit()



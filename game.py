import pygame
from screens import MenuScreen, GameScreen, IntroScreen, GameOver

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("FTL Clone")
        self.clock = pygame.time.Clock()
        self.state = "menu" #menu, intro, game
        self.running = True

        self.menu_screen = MenuScreen(self.screen)
        self.game_screen = GameScreen(self.screen)
        self.intro_screen = IntroScreen(self.screen)
        self.game_over_screen = GameOver(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
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

            # ✅ DRAWING SCREENS
            match self.state:
                case "menu":
                    self.menu_screen.draw()
                case "intro":
                    self.intro_screen.draw(self)
                case "game":
                    self.game_screen.draw(self)
                case "death":
                    self.game_over_screen.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


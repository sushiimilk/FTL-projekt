import pygame
from screens import MenuScreen, GameScreen, IntroScreen

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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    if self.state == "menu":
                        self.menu_screen.handle_event(event, self)
                    elif self.state == "intro":
                        self.intro_screen.handle_event(event, self)
                    elif self.state == "game":
                        self.game_screen.handle_event(event, self)

            if self.state == "menu":
                self.menu_screen.draw()

            elif self.state == "intro":
                self.intro_screen.draw(self)

            elif self.state == "game":
                self.game_screen.draw()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

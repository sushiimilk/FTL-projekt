import pygame

class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface):
        color = (30, 30, 30) if self.is_hovered() else (0, 0, 0)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surf, (self.rect.x + 18, self.rect.y + 2))

class Cursor:
    def __init__(self):
        self.image = pygame.image.load("assets/cursor.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 28))
        pygame.mouse.set_visible(False)

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, pos)

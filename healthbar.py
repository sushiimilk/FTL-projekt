import pygame
from fonts import FONTS

class Bar:
    def __init__(self, x, y, width, height, max_value, fill_color, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        self.fill_color = fill_color
        self.border_color = (255, 255, 255)
        self.background_color = (20, 20, 20)
        self.label = label
        self.font = FONTS["tiny"]

    def update(self, value):
        self.current_value = max(0, min(self.max_value, value))

    def draw(self, surface):
        # Draw label above bar
        if self.label:
            label_surf = self.font.render(self.label, True, (255, 255, 255))
            label_rect = label_surf.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
            surface.blit(label_surf, label_rect)

        # Background
        pygame.draw.rect(surface, self.background_color, self.rect)

        # Filled part
        fill_width = int(self.rect.width * (self.current_value / self.max_value))
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, self.fill_color, fill_rect)

        # Border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        # Value text inside bar
        value_text = f"{self.current_value}/{self.max_value}"
        value_surf = self.font.render(value_text, True, (255, 255, 255))
        value_rect = value_surf.get_rect(center=self.rect.center)
        surface.blit(value_surf, value_rect)
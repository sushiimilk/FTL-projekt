import pygame
from ui import FONT_PATH

pygame.font.init()

FONTS = {
    "huge": pygame.font.Font(FONT_PATH, 50),
    "large": pygame.font.Font(FONT_PATH, 40),
    "medium": pygame.font.Font(FONT_PATH, 28),
    "small": pygame.font.Font(FONT_PATH, 20),
    "tiny": pygame.font.Font(FONT_PATH, 16),
}

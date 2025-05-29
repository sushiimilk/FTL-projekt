import pygame, os, random
from random import randint

pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

#wczytanie grafik
kestrel_sprite_sheet = pygame.image.load('assets/Kestrel Cruiser.png.png').convert_alpha()
#710x489
x, y = 0, 0
width, height = 710, 488
kestrel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
kestrel_surface.blit(kestrel_sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))

# # Save to file (optional)
# pygame.image.save(kestrel_surface, "assets/kestrel.png")

bg = pygame.image.load('assets/Hangar Background.png.jpg')
ship = pygame.image.load('assets/Ship.png')
path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
BACKGROUND = pygame.image.load(os.path.join(path, 'background.png')).convert()
file_names.remove('background.png')
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

#KOLORY
DARKGREEN = pygame.color.THECOLORS['darkgreen']
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
DARKBLUE = pygame.color.THECOLORS['darkblue']
LIGHTBLUE = pygame.color.THECOLORS['lightblue']
DARKRED = pygame.color.THECOLORS['darkred']
LIGHTRED = pygame.color.THECOLORS['pink']
YELLOW = pygame.color.THECOLORS['yellow']

#KLASA GRACZA

class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.level = None


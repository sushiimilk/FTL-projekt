import pygame, os, random
from random import randint

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1200, 700

screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()

#wczytanie grafik
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


import pygame, os, random
from random import randint

pygame.init()

screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

#wczytanie grafik
kestrel_sprite_sheet = pygame.image.load('assets/Kestrel/Kestrel Cruiser.png').convert_alpha()
#~710x489
x, y = 0, 50
width, height = 710, 435
kestrel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
kestrel_surface.blit(kestrel_sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))
# #ZAPISANIE DO PLIKU
# pygame.image.save(kestrel_surface, "assets/kestrel.png")

background = pygame.image.load('assets/Hangar Background.png')

# Fonts
font = pygame.font.SysFont("arial", 40)

# Button
button_rect = pygame.Rect(920, 50, 230, 60)

def draw_entry_screen():
    scaled_background = pygame.transform.scale(background, screen.get_size())
    screen.blit(scaled_background, (0, 0))

    screen.blit(kestrel_surface, (200, -19))  # Adjust position as needed

    pygame.draw.rect(screen, (0, 0, 0), button_rect)
    pygame.draw.rect(screen, (255, 255, 255), button_rect, 1)
    text = font.render("START", True, (255, 255, 255))
    screen.blit(text, (button_rect.x + 10, button_rect.y + 8))

    pygame.display.flip()

#Main loop
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Starting game...")  # Replace with actual game launch
                    return

        draw_entry_screen()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()


# path = os.path.join(os.getcwd(), 'images')
# file_names = os.listdir(path)
# BACKGROUND = pygame.image.load(os.path.join(path, 'background.png')).convert()
# file_names.remove('background.png')
# IMAGES = {}
# for file_name in file_names:
#     image_name = file_name[:-4].upper()
#     IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)
#
# #KOLORY
# DARKGREEN = pygame.color.THECOLORS['darkgreen']
# LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
# DARKBLUE = pygame.color.THECOLORS['darkblue']
# LIGHTBLUE = pygame.color.THECOLORS['lightblue']
# DARKRED = pygame.color.THECOLORS['darkred']
# LIGHTRED = pygame.color.THECOLORS['pink']
# YELLOW = pygame.color.THECOLORS['yellow']
#
# #KLASA GRACZA
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, image, cx, cy):
#         super().__init__()
#         self.level = None
#

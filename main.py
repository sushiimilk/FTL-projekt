import pygame, os, random
from random import randint

pygame.init()
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

# --- WCZYTANIE GRAFIK ---
background = pygame.image.load('assets/Hangar Background.png')
background = pygame.transform.scale(background, screen.get_size())

kestrel_surface = pygame.image.load('assets/Kestrel/Kestrel Cruiser closed.png').convert_alpha()
cursor_img = pygame.image.load('assets/cursor.png').convert_alpha()
cursor_img = pygame.transform.scale(cursor_img, (20,28))
# pygame.mouse.set_visible(False)  # Hide system cursor

# --- FONT ---
font = pygame.font.SysFont("arial", 40)

# --- BUTTON ---
button_rect = pygame.Rect(1020, 50, 130, 60)

# --- DRAW EKRAN STARTOWY ---
def draw_entry_screen():
    screen.blit(background, (0, 0))
    screen.blit(kestrel_surface, (200, -18))  # Adjust ship position as needed

    # Detect hover
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = button_rect.collidepoint(mouse_pos)

    # Button colors
    button_color = (30, 30, 30) if is_hovered else (0, 0, 0)
    border_color = (255, 255, 255)
    text_color = (255, 255, 255)

    # Draw button
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, border_color, button_rect, 2)

    text = font.render("START", True, text_color)
    screen.blit(text, (button_rect.x + 10, button_rect.y + 8))

    # Draw custom cursor
    cursor_offset = (0, 0)  # Change to (x, y) if you want to shift the image
    screen.blit(cursor_img, (mouse_pos[0] - cursor_offset[0], mouse_pos[1] - cursor_offset[1]))

    pygame.display.flip()

# --- MAIN MENU LOOP ---
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Starting game...")  # Replace with actual game logic
                    return

        draw_entry_screen()
        clock.tick(60)

# --- MAIN ---
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

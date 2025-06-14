import pygame, time

class Ship:
    def __init__(self, image_path, x, y, max_health=100, max_shield=50, scale=0.7):
        #pełny rozmiar
        original = pygame.image.load(image_path).convert_alpha()
        w, h = original.get_size()
        self.full_image = original

        #combat rozmiar
        self.scaled_image = pygame.transform.smoothscale(original, (int(w * scale), int(h * scale)))

        self.image = original

        self.rect = self.scaled_image.get_rect(center=(x, y))

        self.shield_fade_alpha = 255
        self.shield_fade_start_time = None
        self.shield_fade_duration = 0.5

        self.shield_image = pygame.image.load("assets/Kestrel/Kestrel Shield.png").convert_alpha()
        shield_w, shield_h = self.shield_image.get_size()
        self.shield_image_scaled = pygame.transform.smoothscale(
            self.shield_image, (int(shield_w * scale), int(shield_h * scale))
        )

        self.health = max_health
        self.max_health = max_health
        self.shield = max_shield
        self.max_shield = max_shield

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def take_damage(self, amount):
        if self.shield > 0:
            blocked = min(self.shield, amount)
            self.shield -= blocked
            amount -= blocked
            if self.shield <= 0 and self.shield_fade_start_time is None:
                self.shield_fade_start_time = time.time()

        if amount > 0:
            self.health -= amount

    def draw(self, surface, centered = False, show_shield=True):
        #rysowanie albo pełnego albo skalowanego statku
        if centered:
            image = self.full_image
            rect = image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        else:
            image = self.scaled_image
            rect = self.rect

        #Rysowanie tarczy
        if show_shield:
            if self.shield > 0:
                shield_img = self.shield_image if centered else self.shield_image_scaled
                shield_rect = shield_img.get_rect(center=rect.center)
                surface.blit(shield_img, shield_rect)

            elif self.shield_fade_start_time:
                elapsed = time.time() - self.shield_fade_start_time
                if elapsed < self.shield_fade_duration:
                    alpha = int(255 * (1 - elapsed / self.shield_fade_duration))
                    shield_img = self.shield_image if centered else self.shield_image_scaled
                    fading_img = shield_img.copy()
                    fading_img.set_alpha(alpha)
                    shield_rect = fading_img.get_rect(center=rect.center)
                    surface.blit(fading_img, shield_rect)
                else:
                    self.shield_fade_start_time = None

        surface.blit(image, rect)

class EnemyShip(Ship):
    def __init__(self, image_path, x, y, max_health=100, max_shield=50):
        original = pygame.image.load(image_path).convert_alpha()
        ow, oh = original.get_size()
        max_width, max_height = 400, 500

        scale_x = max_width / ow
        scale_y = max_height / oh
        scale = min(scale_x, scale_y, 1.0)

        super().__init__(image_path, x, y, max_health, max_shield, scale)
        self.image = self.scaled_image

    def take_damage(self, amount):
        super().take_damage(amount)

    def draw(self, surface, centered=False, show_shield=False):
        super().draw(surface, centered=centered, show_shield=show_shield)
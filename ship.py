import pygame

class Ship:
    def __init__(self, image_path, x, y, max_health=100, max_shield=50, scale=0.7):
        #pełny rozmiar
        original = pygame.image.load(image_path).convert_alpha()
        w, h = original.get_size()
        self.full_image = original

        #combat rozmiar
        self.scaled_image = pygame.transform.smoothscale(original, ((int(w * scale), int(h * scale))))

        self.image = original

        self.rect = self.scaled_image.get_rect(center=(x, y))

        self.shield_image = pygame.image.load("assets/Kestrel/Kestrel Shield.png").convert_alpha()
        shield_w, shield_h = self.shield_image.get_size()
        self.shield_image_scaled = pygame.transform.smoothscale(
            self.shield_image, (int(shield_w * scale), int(shield_h * scale))
        )

        self.health = max_health
        self.max_health = max_health
        self.shield = max_shield
        self.max_shield = max_shield


    def draw(self, surface, centered = False):
        #rysowanie albo pełnego albo skalowanego statku
        if centered:
            image = self.full_image
            rect = image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        else:
            image = self.scaled_image
            rect = self.rect

        #Rysowanie tarczy
        if self.shield > 0:
            if centered:
                shield_img = self.shield_image
                shield_rect = shield_img.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            else:
                shield_img = self.shield_image_scaled
                shield_rect = shield_img.get_rect(center=self.rect.center)

            surface.blit(shield_img, shield_rect)

        surface.blit(image, rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def take_damage(self, amount):
        if self.shield > 0:
            damage_to_shield = min(self.shield, amount)
            self.shield -= damage_to_shield
            amount -= damage_to_shield
        if amount > 0:
            self.health -= amount

class EnemyShip(Ship):
    def __init__(self, image_path, x, y, max_health = 100, max_shield = 50):
        super().__init__(image_path,x,y)
        self.health = max_health
        self.max_health = max_health
        self.shield = max_shield
        self.max_shield = max_shield

    def take_damage(self, amount):
        super().take_damage(amount)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
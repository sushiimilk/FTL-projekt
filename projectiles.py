import pygame

class Projectile:
    def __init__(self, x, y, dx, image_path, damage, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        # Normalize direction and multiply by speed
        length = (dx ** 2) ** 0.5
        if length != 0:
            self.dx = dx / length * speed
        else:
            self.dx = 0
        self.damage = damage
        self.active = True

    def update(self):
        self.rect.x += self.dx
        # Usuń jak poza ekranem
        if self.rect.right < 0 or self.rect.left > 1200:
            self.active = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class LaserProjectile(Projectile):
    def __init__(self, x, y, dx, image_path, damage):
        super().__init__(x, y, dx, image_path, damage, speed=18)  # Laser speed

class RocketProjectile(Projectile):
    def __init__(self, x, y, dx, image_path, damage):
        super().__init__(x, y, dx, image_path, damage, speed=8)   # Rocket speed

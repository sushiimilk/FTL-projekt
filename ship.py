import pygame

class Ship:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class EnemyShip:
    def __init__(self, image_path, x, y, max_health = 100, max_shield = 50):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.health = max_health
        self.max_health = max_health
        self.shield = max_shield
        self.max_shield = max_shield

    def take_damage(self, amount):
        if self.shield > 0:
            damage_to_shield = min(self.shield, amount)
            self.shield -= damage_to_shield
            amount -= damage_to_shield
        if amount > 0:
            self.health -= amount

    def draw(self, surface):
        surface.blit(self.image, self.rect)
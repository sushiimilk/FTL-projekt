import pygame

class Ship:
    def __init__(self, image_path, x, y, max_health=100, max_shield=50):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.shield_image = pygame.image.load("assets/Kestrel/Kestrel Shield.png").convert_alpha()
        self.health = max_health
        self.max_health = max_health
        self.shield = max_shield
        self.max_shield = max_shield


    def draw(self, surface):
        #Rysowanie tarczy
        if self.shield > 0:
            shield_rect = self.shield_image.get_rect(center=self.rect.center)
            surface.blit(self.shield_image, shield_rect)
        surface.blit(self.image, self.rect)
        
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
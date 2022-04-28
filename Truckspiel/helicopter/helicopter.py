from random import randrange
import pygame


class Helikopter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ressources\heli.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(-500, 500))
        self.position = pygame.math.Vector2((self.rect.x, self.rect.y))
        self.type = type
        self.speed = 2

    def respawn(self):
        self.position = pygame.math.Vector2(
            randrange(-500, 200, 10), randrange(800, 1000, 10)
        )

    def move(self, playerpos):
        self.vector_player = pygame.math.Vector2(playerpos)
        self.vector_richtung = (self.vector_player - self.position).normalize()  # Doku
        self.position += self.vector_richtung.elementwise() * self.speed
        self.rect.center = self.position.xy

    def PlayerinArea(self, player_rect):
        return self.rect.colliderect(player_rect)

    def Set_Speed(self, value):
        self.speed += value

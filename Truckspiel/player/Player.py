import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ressources\car-truck4.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.tankfullstand = 2000
        self.lager = 0

    def player_input(self):
        if self.tankfullstand > 0:
            keys = pygame.key.get_pressed()
            playerspeed = 3
            y_change = 0
            x_change = 0
            if keys[pygame.K_w] and keys[pygame.K_a]:
                y_change = -playerspeed
                x_change = -playerspeed
            if keys[pygame.K_w] and keys[pygame.K_d]:
                y_change = -playerspeed
                x_change = playerspeed
            if keys[pygame.K_w]:
                y_change = -playerspeed
            if keys[pygame.K_s] and keys[pygame.K_a]:
                y_change = playerspeed
                x_change = -playerspeed
            if keys[pygame.K_s] and keys[pygame.K_d]:
                y_change = playerspeed
                x_change = playerspeed
            if keys[pygame.K_s]:
                y_change = playerspeed
            if keys[pygame.K_d]:
                x_change += playerspeed
            if keys[pygame.K_a]:
                x_change = -playerspeed

            if (
                keys[pygame.K_s]
                or keys[pygame.K_d]
                or keys[pygame.K_w]
                or keys[pygame.K_a]
            ):
                self.verbrauch()

            self.rect.x += x_change
            self.rect.y += y_change

    def tanken(
        self,
    ):
        if self.tankfullstand <= 5000:
            if (self.tankfullstand + 20) > 5000:
                self.tankfullstand -= 5000 - self.tankfullstand
            else:
                self.tankfullstand += 20

    def verbrauch(self):
        if self.tankfullstand > 0:
            self.tankfullstand -= 5

    def abbauen(self, erzlagerkapa):
        if self.lager < 100 and erzlagerkapa >= 0:
            self.lager += 0.2

    def lagern(self):
        if self.lager > 0:
            self.lager -= 0.2

    def wareverloren(self):
        self.lager = 0

    def update(self):
        self.player_input()

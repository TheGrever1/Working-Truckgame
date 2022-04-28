import pygame


class AnzeigeMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 25)

    def text_surf(self, amount, string):
        self.tankfullstand_player_surf = self.font.render(
            "%s: %d" % (string, amount), True, "Black"
        )
        return self.tankfullstand_player_surf

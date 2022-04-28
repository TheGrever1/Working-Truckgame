import pygame
from sys import exit
from game import *

pygame.init()

screen = pygame.display.set_mode((1260, 930))
clock = pygame.time.Clock()
pygame.display.set_caption("Truckspiel")
game = Game(screen, clock)

game.game_loop()

pygame.quit()
exit()

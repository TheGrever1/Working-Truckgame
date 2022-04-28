from typing import List
import pygame
import pygame_menu
from sys import exit
from Map.Anzeige import AnzeigeMenu
from Map.buildings import *
from player.Player import *
from helicopter.helicopter import *
from gamestate import *

pygame.init()

screen = pygame.display.set_mode((1260, 930))
clock = pygame.time.Clock()
pygame.display.set_caption("Truckspiel")

erzabbau_usage = Erzabbaustelle()
erzlager_usage = Erzlager()
tankstelle_usage = Tankstelle()
heli_usage = Helikopter()
player_usage = Player()
player = pygame.sprite.GroupSingle()
player.add(player_usage)
object_group = pygame.sprite.Group()
menu_surfaces = AnzeigeMenu()
gamestate = Gamestate.menu


def collision_sprite():
    if tankstelle_usage.PlayerinArea(player_usage.rect):
        tankstelle_usage.tanken(player_usage.tankfullstand)
        player_usage.tanken()
    if erzabbau_usage.PlayerinArea(player_usage.rect):
        player_usage.abbauen(erzabbau_usage.vorkommen)
        erzabbau_usage.abbauen(player_usage.lager)
    if erzlager_usage.PlayerinArea(player_usage.rect):
        erzlager_usage.lagern(player_usage.lager)
        player_usage.lagern()
    if heli_usage.PlayerinArea(player_usage.rect):
        heli_usage.respawn()
        player_usage.wareverloren()


def set_difficulty(value, difficulty):
    heli_usage.Set_Speed(value[1])


def menu(text):
    screen = pygame.display.set_mode((400, 300))
    menu = pygame_menu.Menu(
        "Transporter", 400, 300, theme=pygame_menu.themes.THEME_DARK
    )

    menu.add.label(text)
    menu.add.selector(
        "Difficulty :", [("Hard", 1), ("Easy", 2)], onchange=set_difficulty
    )
    menu.add.button("Play", game_loop)
    menu.add.button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)


def game_loop():
    screen = pygame.display.set_mode((1260, 930))
    gamestate = Gamestate.playing
    object_group.add(tankstelle_usage)
    object_group.add(erzabbau_usage)
    object_group.add(erzlager_usage)
    object_group.add(heli_usage)

    while gamestate == Gamestate.playing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = Gamestate.menu
            if player_usage.tankfullstand == 0:
                gamestate = Gamestate.gameover
        if (player_usage.lager + erzabbau_usage.vorkommen + erzlager_usage.lager) <= (
            erzabbau_usage.maxvorkommen / 100
        ) * 80:
            gamestate = Gamestate.gameover
        elif (erzlager_usage.lager) >= (erzabbau_usage.maxvorkommen / 100) * 80:
            gamestate = Gamestate.gewonnen

        collision_sprite()
        heli_usage.move(player_usage.rect.center)
        screen.fill((255, 255, 255))
        object_group.draw(screen)
        object_group.update()
        player.draw(screen)
        player.update()
        screen.blit(
            menu_surfaces.text_surf(player_usage.tankfullstand, "Tank"),
            (10, 800),
        )
        screen.blit(
            menu_surfaces.text_surf(tankstelle_usage.tank, "Tankstelle"),
            (10, 825),
        )
        screen.blit(
            menu_surfaces.text_surf(player_usage.lager, "Lager"),
            (10, 850),
        )
        screen.blit(
            menu_surfaces.text_surf(erzabbau_usage.vorkommen, "Erzquelle"),
            (10, 875),
        )
        screen.blit(
            menu_surfaces.text_surf(erzlager_usage.lager, "Warehouselager"),
            (10, 900),
        )
        pygame.display.update()
        clock.tick(60)
    if gamestate == Gamestate.gameover:
        menu("Verloren")
    if gamestate == Gamestate.menu:
        menu("")
    if gamestate == Gamestate.gewonnen:
        menu("Gewonnen!")


menu("Wilkommen")
pygame.quit()
exit()

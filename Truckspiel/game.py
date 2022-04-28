import pygame
import pygame_menu
from Map.Anzeige import AnzeigeMenu
from Map.buildings import *
from player.Player import *
from gamestate import *

from helicopter.helicopter import *


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.menu("Wilkommen")

    def game_loop(self):
        self.helicopter = Helikopter()
        self.tankstelle = Tankstelle()
        self.erzabbauch = Erzabbaustelle()
        self.erzlager = Erzlager()
        self.player_usage = Player()
        self.screen = pygame.display.set_mode((1260, 930))
        gamestate = Gamestate.playing
        self.player = pygame.sprite.GroupSingle()
        self.player.add(self.player_usage)
        object_group = pygame.sprite.Group()
        menu_surfaces = AnzeigeMenu()

        object_group.add(self.tankstelle)
        object_group.add(self.erzabbauch)
        object_group.add(self.erzlager)
        object_group.add(self.helicopter)

        while gamestate == Gamestate.playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamestate = Gamestate.menu
                if self.player_usage.tankfullstand == 0:
                    gamestate = Gamestate.gameover
            if (
                self.player_usage.lager
                + self.erzabbauch.vorkommen
                + self.erzlager.lager
            ) <= (self.erzabbauch.maxvorkommen / 100) * 80:
                gamestate = Gamestate.gameover
            elif (self.erzlager.lager) >= (self.erzabbauch.maxvorkommen / 100) * 80:
                gamestate = Gamestate.gewonnen

            self.collision_sprite()
            self.helicopter.move(self.player_usage.rect.center)
            self.screen.fill((255, 255, 255))
            object_group.draw(self.screen)
            object_group.update()
            self.player.draw(self.screen)
            self.player.update()
            self.screen.blit(
                menu_surfaces.text_surf(self.player_usage.tankfullstand, "Tank"),
                (10, 800),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.tankstelle.tank, "Tankstelle"),
                (10, 825),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.player_usage.lager, "Lager"),
                (10, 850),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.erzabbauch.vorkommen, "Erzquelle"),
                (10, 875),
            )
            self.screen.blit(
                menu_surfaces.text_surf(self.erzlager.lager, "Warehouselager"),
                (10, 900),
            )
            pygame.display.update()
            self.clock.tick(60)
        if gamestate == Gamestate.gameover:
            self.menu("Verloren")
        if gamestate == Gamestate.menu:
            self.menu("")
        if gamestate == Gamestate.gewonnen:
            self.menu("Gewonnen!")

    def collision_sprite(self):
        if self.tankstelle.PlayerinArea(self.player_usage.rect):
            self.tankstelle.tanken(self.player_usage.tankfullstand)
            self.player_usage.tanken()
        if self.erzabbauch.PlayerinArea(self.player_usage.rect):
            self.player_usage.abbauen(self.erzabbauch.vorkommen)
            self.erzabbauch.abbauen(self.player_usage.lager)
        if self.erzlager.PlayerinArea(self.player_usage.rect):
            self.erzlager.lagern(self.player_usage.lager)
            self.player_usage.lagern()
        if self.helicopter.PlayerinArea(self.player_usage.rect):
            self.helicopter.respawn()
            self.player_usage.wareverloren()

    def menu(self, text):
        self.screen = pygame.display.set_mode((400, 300))
        menu = pygame_menu.Menu(
            "Transporter", 400, 300, theme=pygame_menu.themes.THEME_DARK
        )

        menu.add.label(text)
        menu.add.selector(
            "Difficulty :", [("Easy", 1), ("Hard", 2)], onchange=self.set_difficulty
        )
        menu.add.button("Play", self.game_loop)
        menu.add.button("Quit", pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def set_difficulty(self, value, difficulty):
        self.helicopter.Set_Speed(value[1])

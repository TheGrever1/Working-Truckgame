from enum import Enum

import enum

class Gamestate(enum.Enum):
    menu = 0
    playing = 1
    gameover = 2
    
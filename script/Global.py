import pygame
import numpy
from enum import Enum

# Enum


class GameState(Enum):
    playing = 0
    winning = 1
    end = 2


class Layer(Enum):
    default = 0
    block = 1
    board = 2
    UI = 3


class TypeBlock(Enum):
    target = 0
    normal = 1
    unmovable = 2
    slip = 3


class TypeDirection(Enum):
    horizontal = 1
    vertical = 2


# Constant
FPS = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
BOARD_SIZE = 6
BOARD_POSITION = (330, 30)
SQUARE_SIZE = 90
SHADOW_SIZE = 5
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
BLOCK_MOVE_SPEED = 4
MAX_LEVEL = 32
ENCODE = 255

# Screen Init
spr_icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(spr_icon)
pygame.display.set_caption("Unblock It")
screen = pygame.display.set_mode(SCREEN_SIZE)

# Basic Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global Attributes
delta_time = 0.0
getTicksLastFrame = 0.0
GAME_STATE = GameState.playing
MATRIX: numpy.ndarray = numpy.zeros((0, 0))
OLD_MATRIX: numpy.ndarray = numpy.zeros((0, 0))

# Global Methods


def real_position(grid_pos):
    grid_pos = list(grid_pos)
    x = BOARD_POSITION[0] + grid_pos[1] * SQUARE_SIZE
    y = BOARD_POSITION[1] + grid_pos[0] * SQUARE_SIZE
    return x, y


def grid_position(real_pos):
    real_pos = list(real_pos)
    i = round((real_pos[1] - BOARD_POSITION[1]) / float(SQUARE_SIZE))
    j = round((real_pos[0] - BOARD_POSITION[0]) / float(SQUARE_SIZE))
    return i, j


def sign(value):
    if value < 0:
        return -1
    elif value > 0:
        return 1
    return 0
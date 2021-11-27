import pygame
import Global
from script.Level import *
from script.Entity import *
from script.Global import *
from script.GameController import *
from script.UI import UserInterface


game_running = True # The game has started running

pygame.init()

# Game loader
GameLoader() # Must call fisrt

# Game controller
GameController()

# Level Comtroller
level_controller = LevelController(BOARD_SIZE, BOARD_SIZE)

# UI
UserInterface(level_controller)

# Mouse cursor
pygame.mouse.set_cursor(*pygame.cursors.arrow)

# Game state
Global.GAME_STATE = GameState.playing

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            GameController.mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            GameController.mouse_up = True

    screen.fill(BLACK)

    GameController.update()
    level_controller.update()
    GameController.render()

    pygame.display.flip()

    # Delta Time
    t = pygame.time.get_ticks()
    Global.delta_time = (t - getTicksLastFrame)/1000.0
    getTicksLastFrame = t

    pygame.time.Clock().tick(FPS)


pygame.quit()
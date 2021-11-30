# import pygame
import pickle

import pygame.image

import Global
from script.Global import *
from abc import ABC, abstractmethod


class PlayerData:
    level_reached = 1
    play_sound = True
    play_music = True
    best_moves = ""

    def __init__(self, lvl, ps, pm):
        self.level_reached = lvl
        self.play_sound = ps
        self.play_music = pm
        for i in range(Global.MAX_LEVEL):
            self.best_moves += chr(Global.ENCODE)

"""
    Loading all sprites that using in high frequency
"""


class GameLoader:
    LOADER = {}
    PDATA: PlayerData = PlayerData(1, True, True)

    def __init__(self):
        self.LOADER["spr_icon"] = pygame.image.load("image/icon.png")
        self.LOADER["spr_target_block"] = pygame.image.load("image/target_block.png")
        self.LOADER["spr_block_1x2"] = pygame.image.load("image/normal_block_1x2.png")
        self.LOADER["spr_block_1x3"] = pygame.image.load("image/normal_block_1x3.png")
        self.LOADER["spr_block_2x1"] = pygame.image.load("image/normal_block_2x1.png")
        self.LOADER["spr_block_3x1"] = pygame.image.load("image/normal_block_3x1.png")
        self.LOADER["spr_steel_block_1x1"] = pygame.image.load("image/steel_block_1x1.png")
        self.LOADER["spr_steel_block_1x2"] = pygame.image.load("image/steel_block_1x2.png")
        self.LOADER["spr_steel_block_1x3"] = pygame.image.load("image/steel_block_1x3.png")
        self.LOADER["spr_steel_block_2x1"] = pygame.image.load("image/steel_block_2x1.png")
        self.LOADER["spr_steel_block_3x1"] = pygame.image.load("image/steel_block_3x1.png")
        self.LOADER["spr_border"] = pygame.image.load("image/border.png")
        self.LOADER["spr_background"] = pygame.image.load("image/background.jpg")
        self.LOADER["spr_board_background"] = pygame.image.load("image/board_background.jpg")
        self.LOADER["spr_glass_block_1x1"] = pygame.image.load("image/glass_block_1x1.png")
        self.LOADER["spr_glass_block_1x2"] = pygame.image.load("image/glass_block_1x2.png")
        self.LOADER["spr_glass_block_1x3"] = pygame.image.load("image/glass_block_1x3.png")
        self.LOADER["spr_glass_block_2x1"] = pygame.image.load("image/glass_block_2x1.png")
        self.LOADER["spr_glass_block_3x1"] = pygame.image.load("image/glass_block_3x1.png")
        self.LOADER["spr_sound"] = pygame.image.load("image/btn_sound.png")
        self.LOADER["spr_music"] = pygame.image.load("image/btn_music.png")
        self.LOADER["spr_no_sound"] = pygame.image.load("image/btn_no_sound.png")
        self.LOADER["spr_no_music"] = pygame.image.load("image/btn_no_music.png")
        self.LOADER["spr_level_lock"] = pygame.image.load("image/level_lock.png")
        self.LOADER["spr_level_unlock"] = pygame.image.load("image/level_unlock.png")
        self.LOADER["spr_level_completed"] =\
            pygame.transform.scale(pygame.image.load("image/level_completed.png"), (602, 95))
        self.load_audios()
        self.load_game()

    def load_audios(self):
        self.LOADER["ui_click"] = pygame.mixer.Sound("audio/ui_click.wav")
        self.LOADER["win"] = pygame.mixer.Sound("audio/win.wav")
        self.LOADER["block_placed"] = pygame.mixer.Sound("audio/block_placed.wav")
        self.LOADER["ignore"] = pygame.mixer.Sound("audio/ignore.wav")
        pygame.mixer.music.load("audio/game_theme.wav")

    @staticmethod
    def save_game():
        with open("level/save.txt", "wb") as f:
            pickle.dump(GameLoader.PDATA, f)

    @staticmethod
    def load_game():
        # GameLoader.save_game()  # Uncomment and play to reset data
        with open("level/save.txt", "rb") as f:
            GameLoader.PDATA = pickle.load(f)
        if GameLoader.PDATA.play_music:
            pygame.mixer.music.play(-1)

"""
    This class is representing a game object
"""


class GameObject(ABC):
    _image: pygame.image = None
    _position: list[float] = [0, 0]
    _layer = Layer.default

    @abstractmethod
    def __init__(self, position=(0, 0)):
        self._position = list(position)
        self._active = True
        GameController.OBJECT.append(self)

    def tick(self):
        if self._active:
            self.update()

    def set_active(self, boolean):
        self._active = boolean

    def get_active(self):
        return self._active

    @abstractmethod
    def update(self):
        pass

    def render(self):
        if self._image is not None and self._active:
            screen.blit(self._image, self._position)

    def destroy(self):
        GameController.OBJECT.remove(self)
        del self

    def get_layer(self):
        return self._layer

"""
    Creating, updating and rendering all of game objects
"""


class GameController:
    OBJECT: list[GameObject] = []
    mouse_down = False
    mouse_up = False
    matrix_changed = False
    old_mouse_position = (0, 0)

    def __init__(self):
        GameController.old_mouse_position = pygame.mouse.get_pos()

    @staticmethod
    def update():
        for obj in GameController.OBJECT:
            obj.tick()
        GameController.mouse_down = GameController.mouse_up = False
        GameController.old_mouse_position = pygame.mouse.get_pos()

    @staticmethod
    def render():
        for obj in GameController.OBJECT:
            if obj.get_layer() != Layer.UI:
                obj.render()
        for obj in GameController.OBJECT:
            if obj.get_layer() == Layer.UI:
                obj.render()

    @staticmethod
    def clear_layer(layer):
        i = len(GameController.OBJECT)
        while i > 0:
            i -= 1
            if GameController.OBJECT[i].get_layer() == layer:
                GameController.OBJECT[i].destroy()
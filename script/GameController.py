# import pygame
import pygame.image

from script.Global import *
from abc import ABC, abstractmethod

"""
    Loading all sprites that using in high frequency
"""


class GameLoader:
    LOADER = {}

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
            obj.render()

    @staticmethod
    def clear_layer(layer):
        i = len(GameController.OBJECT)
        while i > 0:
            i -= 1
            if GameController.OBJECT[i].get_layer() == layer:
                GameController.OBJECT[i].destroy()
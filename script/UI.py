import pygame.mixer

import GameController
import Level
from script.GameController import *


class Button(GameObject):
    lock: bool

    def __init__(self, position, button_id, image=None):
        super(Button, self).__init__(position)
        self._layer = Layer.UI
        self.id = button_id
        self.lock = True
        self.font = pygame.font.Font("font/BRLNSB.ttf", 30)
        self.text = ""
        self.text_color = (0, 0, 0)
        self.text_offset = (0, 0)

        if image is not None:
            self._image = pygame.image.load("image/" + image)

    def set_font_size(self, size):
        self.font = pygame.font.Font("font/BRLNSB.ttf", size)

    def update(self):
        pass
    
    def render(self):
        super(Button, self).render()
        if self.text != "" and self._active:
            text = self.font.render(self.text, True, self.text_color)
            screen.blit(text,
                        (self._position[0] + self.text_offset[0] - text.get_width()/2,
                         self._position[1] + self.text_offset[1]))

    def set_image(self, image):
        self._image = image

    def is_in_mouse_up(self):
        if self.is_below_mouse_position() and GameController.mouse_up:
            if pygame.mouse.get_cursor() != pygame.cursors.broken_x:
                if GameLoader.PDATA.play_sound:
                    pygame.mixer.Sound.play(GameLoader.LOADER["ui_click"])
                GameController.mouse_up = False
                return True
        return False

    def is_in_mouse_down(self):
        if self.is_below_mouse_position() and GameController.mouse_down:
            GameController.mouse_down = False
            return True
        return False

    def is_below_mouse_position(self):
        rect = self._image.get_rect()
        rect.topleft = self._position
        if rect.collidepoint(pygame.mouse.get_pos()):
            self._image.set_alpha(150)
            return True
        else:
            self._image.set_alpha(255)
            return False


class Background(GameObject):

    def __init__(self, position=(0, 0)):
        super(Background, self).__init__(position)
        self._image = GameLoader.LOADER["spr_background"]
        self._image = pygame.transform.scale(self._image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        pass


class UserInterface:
    main_menu = None
    level_menu = None
    options = None
    credits = None
    play_menu = None

    def __init__(self, level: Level.LevelController):
        UserInterface.main_menu = MainMenu((0, 0))
        UserInterface.options = OptionsMenu((0, 0))
        UserInterface.credits = CreditsMenu((0, 0))
        UserInterface.level_menu = LevelMenu((100, 100), level)
        UserInterface.play_menu = GameplayMenu((75, 485), level)
        UserInterface.options.set_active(False)
        UserInterface.credits.set_active(False)
        UserInterface.level_menu.set_active(False)
        UserInterface.play_menu.set_active(False)


class MainMenu(GameObject):

    def __init__(self, position):
        super(MainMenu, self).__init__(position)
        self._layer = Layer.UI
        self.name = Button((SCREEN_WIDTH / 2 - 225, SCREEN_HEIGHT / 2 - 200), 0, "name.png")
        self.btn_play = Button((SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50), 0, "btn_play.png")
        self.btn_options = Button((SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 35), 0, "btn_options.png")
        self.btn_credits = Button((SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 120), 0, "btn_credits.png")

    def update(self):
        if self.btn_play.is_in_mouse_up():
            UserInterface.level_menu.set_active(True)
            self.set_active(False)
        if self.btn_credits.is_in_mouse_up():
            UserInterface.credits.set_active(True)
            self.set_active(False)
        if self.btn_options.is_in_mouse_up():
            UserInterface.options.set_active(True)
            self.set_active(False)

    def set_active(self, boolean):
        super(MainMenu, self).set_active(boolean)
        self.name.set_active(boolean)
        self.btn_play.set_active(boolean)
        self.btn_credits.set_active(boolean)
        self.btn_options.set_active(boolean)


class OptionsMenu(GameObject):

    def __init__(self, position):
        super(OptionsMenu, self).__init__(position)
        self._layer = Layer.UI
        sound_x, sound_y = SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 30
        music_x, music_y = SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 60
        self.setting = Button((SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 200), 0, "setting.png")

        self.btn_save = Button((music_x + 35, music_y + 90), 0, "btn_save.png")

        self.btn_txt_music = Button((music_x, music_y), 0, "btn_txt_music.png")
        self.btn_txt_sound = Button((sound_x, sound_y), 0, "btn_txt_sound.png")

        if GameLoader.PDATA.play_sound:
            self.btn_sound = Button((sound_x + 220, sound_y), 1, "btn_sound.png")
        else:
            self.btn_sound = Button((sound_x + 220, sound_y), 0, "btn_no_sound.png")

        if GameLoader.PDATA.play_music:
            self.btn_music = Button((music_x + 220, music_y), 1, "btn_music.png")
        else:
            self.btn_music = Button((music_x + 220, music_y), 0, "btn_no_music.png")

    def update(self):
        if self.btn_sound.is_in_mouse_up():
            if self.btn_sound.id == 1:
                GameLoader.PDATA.play_sound = False
                self.btn_sound.set_image(GameLoader.LOADER["spr_no_sound"])
                self.btn_sound.id = 0
            else:
                GameLoader.PDATA.play_sound = True
                pygame.mixer.Sound.play(GameLoader.LOADER["ui_click"])
                self.btn_sound.set_image(GameLoader.LOADER["spr_sound"])
                self.btn_sound.id = 1
        if self.btn_music.is_in_mouse_up():
            if self.btn_music.id == 1:
                GameLoader.PDATA.play_music = False
                pygame.mixer.music.stop()
                self.btn_music.set_image(GameLoader.LOADER["spr_no_music"])
                self.btn_music.id = 0
            else:
                GameLoader.PDATA.play_music = True
                pygame.mixer.music.play(-1)
                self.btn_music.set_image(GameLoader.LOADER["spr_music"])
                self.btn_music.id = 1
        if self.btn_save.is_in_mouse_up():
            GameLoader.save_game()
            UserInterface.main_menu.set_active(True)
            self.set_active(False)

    def set_active(self, boolean):
        super(OptionsMenu, self).set_active(boolean)
        self.btn_sound.set_active(boolean)
        self.btn_music.set_active(boolean)
        self.btn_save.set_active(boolean)
        self.btn_txt_music.set_active(boolean)
        self.btn_txt_sound.set_active(boolean)
        self.setting.set_active(boolean)


class CreditsMenu(GameObject):

    def __init__(self, position):
        super(CreditsMenu, self).__init__(position)
        self._layer = Layer.UI
        self.infor = Button((SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 50), 0,  "infor.png")
        self.about = Button((SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 200), 0,  "about.png")
        self.btn_home = Button((SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT - 100), 0, "btn_home.png")

    def update(self):
        if self.btn_home.is_in_mouse_up():
            UserInterface.main_menu.set_active(True)
            self.set_active(False)

    def set_active(self, boolean):
        super(CreditsMenu, self).set_active(boolean)
        self.infor.set_active(boolean)
        self.about.set_active(boolean)
        self.btn_home.set_active(boolean)


class LevelMenu(GameObject):
    level_buttons: list[Button] = []

    def __init__(self, position, level: Level.LevelController):
        super(LevelMenu, self).__init__(position)
        self._position = position
        self._layer = Layer.UI
        self.level = level
        self.level.lvl_select = self
        d = 90
        self.btn_home = Button((SCREEN_WIDTH/2 - 30, SCREEN_HEIGHT - 100), 0, "btn_home.png")
        for i in range(0, 4):
            for j in range(0, 8):
                self.level_buttons.append(Button((self._position[0] + d*j, self._position[1] + d*i), 8*i+j+1,
                                                 "level_lock.png"))
        self.level_buttons[0].lock = False

    def update(self):
        if self.btn_home.is_in_mouse_up():
            UserInterface.main_menu.set_active(True)
            self.set_active(False)
        for button in self.level_buttons:
            if not button.lock:
                if button.text == "":
                    button.text = str(button.id).zfill(2)
                    button.text_offset = (35, 13)
                    button.set_image(pygame.image.load("image/level_unlock.png"))
                if button.is_in_mouse_up():
                    self.set_active(False)
                    self.level.load_level(button.id)
                    UserInterface.play_menu.set_active(True)

    def set_active(self, boolean):
        super(LevelMenu, self).set_active(boolean)
        self.btn_home.set_active(boolean)
        for button in self.level_buttons:
            button.set_active(boolean)
            if button.id <= GameLoader.PDATA.level_reached:
                button.lock = False


class GameplayMenu(GameObject):

    def __init__(self, position, level):
        super(GameplayMenu, self).__init__(position)
        self._layer = Layer.UI
        self.level = level
        self.move = 0
        self.level.ui = self

        # LVL COMPLETED
        self.level_completed = Button((298, 250), 0)
        self.level_completed.set_image(GameLoader.LOADER["spr_level_completed"])
        self.level_completed.set_active(False)

        # LEVEL Area
        self.level_display = Button((35, 50), 0, "round_border.png")
        self.level_display.text = "LEVEL"
        self.level_display.text_color = (255, 255, 255)
        self.level_display.text_offset = (120, 10)
        self.level_text = Button((35, 100), 0)
        self.level_text.set_font_size(50)
        self.level_text.text_color = (255, 255, 255)
        self.level_text.text_offset = (120, 0)

        # BEST Area
        self.best_display = Button((35, 190), 0, "round_border.png")
        self.best_display.text = "BEST"
        self.best_display.text_color = (255, 255, 255)
        self.best_display.text_offset = (120, 10)
        self.best_text = Button((35, 240), 0)
        self.best_text.set_font_size(50)
        self.best_text.text_color = (255, 255, 255)
        self.best_text.text_offset = (120, 0)

        # CURR Area
        self.curr_display = Button((35, 330), 0, "round_border.png")
        self.curr_display.text = "CURR"
        self.curr_display.text_color = (255, 255, 255)
        self.curr_display.text_offset = (120, 10)
        self.curr_text = Button((35, 380), 0)
        self.curr_text.set_font_size(50)
        self.curr_text.text_color = (255, 255, 255)
        self.curr_text.text_offset = (120, 0)

        self.btn_home = Button(position, 0, "btn_home.png")
        self.btn_reload = Button((position[0] + 85, position[1]), 0, "btn_reload.png")

    def update(self):
        if self.btn_home.is_in_mouse_up():
            UserInterface.main_menu.set_active(True)
            UserInterface.level_menu.level.hide_board()
            GameController.clear_layer(Layer.block)
            self.set_active(False)
        if self.btn_reload.is_in_mouse_up():
            self.level.restart_level()
        if GameController.matrix_changed:
            GameController.matrix_changed = False
            self.move += 1
            self.curr_text.text = str(self.move).zfill(2)
        if Global.GAME_STATE == GameState.winning:
            self.level_completed.set_active(True)
            best = ord(GameLoader.PDATA.best_moves[self.level.level - 1]) - ENCODE
            if best == 0 or best > self.move:
                list_best_moves = list(GameLoader.PDATA.best_moves)
                list_best_moves[self.level.level - 1] = chr(self.move + ENCODE)
                GameLoader.PDATA.best_moves = "".join(list_best_moves)
                self.best_text.text = str(self.move).zfill(2)

    def set_active(self, boolean):
        super(GameplayMenu, self).set_active(boolean)
        self.btn_home.set_active(boolean)
        self.btn_reload.set_active(boolean)
        self.curr_text.set_active(boolean)
        self.level_text.set_active(boolean)
        self.best_text.set_active(boolean)
        self.best_display.set_active(boolean)
        self.level_display.set_active(boolean)
        self.curr_display.set_active(boolean)
        self.move = 0
        self.level_completed.set_active(False)
        self.level_text.text = str(self.level.level).zfill(2)
        self.curr_text.text = str(self.move).zfill(2)
        best = ord(GameLoader.PDATA.best_moves[self.level.level - 1]) - ENCODE
        if best != 0:
            self.best_text.text = str(best).zfill(2)
        else:
            self.best_text.text = "--"
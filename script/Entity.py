import pygame.transform
import math
from script.GameController import *
import Global


class Board(GameObject):

    def __init__(self, position):
        self._image = pygame.transform.scale(GameLoader.LOADER["spr_board_background"],
                                             (BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE + 30))
        self._image = pygame.transform.rotate(self._image, 90)
        super(Board, self).__init__(position)

    def update(self):
        pass


class Border(GameObject):

    def __init__(self, position):
        self._image = pygame.transform.scale(GameLoader.LOADER["spr_border"],
                                             (608 + SHADOW_SIZE, 608 + SHADOW_SIZE))
        # self._image = pygame.transform.rotate(self._image, 90)
        super(Border, self).__init__(position)

    def update(self):
        pass


class WoodBlock(GameObject):
    """
        Move this block around to make way for target block go out
    """

    def __init__(self, position, size):
        super(WoodBlock, self).__init__(position)
        self._layer = Layer.block
        size = list(size)
        if size[0] > size[1]:
            self._type = TypeDirection.horizontal
        else:
            self._type = TypeDirection.vertical
        self._size = size
        self._is_holding = False
        self._image = self.block_image(size)
        self._delta = 0
        self.fill_matrix(1)
        self._limit = [BOARD_POSITION[0],
                       BOARD_POSITION[1],
                       BOARD_POSITION[0] + SQUARE_SIZE * BOARD_SIZE,
                       BOARD_POSITION[1] + SQUARE_SIZE * BOARD_SIZE
                       ]

    def fill_matrix(self, value):
        grid_pos = grid_position(self._position)
        for i in range(self._size[1]):
            for j in range(self._size[0]):
                Global.MATRIX[grid_pos[0] + i][grid_pos[1] + j] = value

    def bound(self):
        x1 = self._position[0]
        y1 = self._position[1]
        x2 = self._position[0] + self._size[0] * SQUARE_SIZE
        y2 = self._position[1] + self._size[1] * SQUARE_SIZE
        return x1, y1, x2, y2

    def is_below_mouse_position(self):
        m_x, m_y = pygame.mouse.get_pos()
        bound = list(self.bound())
        if bound[0] < m_x < bound[2] and bound[1] < m_y < bound[3]:
            return True
        return False

    def auto_align_to_grid(self):
        xx = BOARD_POSITION[0] + round((self._position[0] - BOARD_POSITION[0]) / float(SQUARE_SIZE)) * SQUARE_SIZE
        yy = BOARD_POSITION[1] + round((self._position[1] - BOARD_POSITION[1]) / float(SQUARE_SIZE)) * SQUARE_SIZE
        self._position[0] += (xx - self._position[0]) / 2.0
        self._position[1] += (yy - self._position[1]) / 2.0

        if math.fabs(xx - self._position[0]) < 3:
            self._position[0] = xx

        if math.fabs(yy - self._position[1]) < 3:
            self._position[1] = yy

    def calculate_limit(self):
        # Default limit
        self._limit = [BOARD_POSITION[0],
                       BOARD_POSITION[1],
                       BOARD_POSITION[0] + SQUARE_SIZE * BOARD_SIZE,
                       BOARD_POSITION[1] + SQUARE_SIZE * BOARD_SIZE
                       ]
        # left - top - right - down
        i, j = grid_position(self._position)
        if self._type == TypeDirection.vertical:
            while i > 0:
                i -= 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[1] = real_position((i + 1, j))[1]
                    break
            while i < BOARD_SIZE - 1:
                i += 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[3] = real_position((i, j))[1]
                    break
        else:
            while j > 0:
                j -= 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[0] = real_position((i, j + 1))[0]
                    break
            while j < BOARD_SIZE - 1:
                j += 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[2] = real_position((i, j))[0]
                    break

    def limit_position(self):
        bound = list(self.bound())
        if bound[0] < self._limit[0]:
            self._position[0] = self._limit[0]
        if bound[1] < self._limit[1]:
            self._position[1] = self._limit[1]
        if bound[2] > self._limit[2]:
            self._position[0] = self._limit[2] - self._size[0] * SQUARE_SIZE
        if bound[3] > self._limit[3]:
            self._position[1] = self._limit[3] - self._size[1] * SQUARE_SIZE

    def set_holding(self, value):
        self._is_holding = value
        if self._is_holding:
            Global.OLD_MATRIX = Global.MATRIX.copy()
            self.fill_matrix(0)
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            self.calculate_limit()
        else:
            self.fill_matrix(1)
            if not numpy.array_equal(Global.MATRIX, Global.OLD_MATRIX):
                GameController.matrix_changed = True
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if GameLoader.PDATA.play_sound:
                pygame.mixer.Sound.play(GameLoader.LOADER["block_placed"])

    def update(self):
        m_x, m_y = pygame.mouse.get_pos()

        # Check if mouse is holding this block
        if GameController.mouse_down and pygame.mouse.get_cursor() != pygame.cursors.broken_x:
            if self.is_below_mouse_position():
                self.set_holding(True)
                if self._type == TypeDirection.horizontal:
                    self._delta = self._position[0] - m_x
                else:
                    self._delta = self._position[1] - m_y

        if GameController.mouse_up and self._is_holding:
            self.set_holding(False)

        # Move
        if self._is_holding:
            if self._type == TypeDirection.horizontal:
                self._position[0] += ((m_x + self._delta) - self._position[0]) / 10.0 * BLOCK_MOVE_SPEED
            else:
                self._position[1] += ((m_y + self._delta) - self._position[1]) / 10.0 * BLOCK_MOVE_SPEED
        self.limit_position()

        # Auto align
        if not self._is_holding:
            self.auto_align_to_grid()

    @staticmethod
    def block_image(size):
        size = list(size)

        if size == [1, 2]:
            image = GameLoader.LOADER["spr_block_1x2"]
        elif size == [1, 3]:
            image = GameLoader.LOADER["spr_block_1x3"]
        elif size == [2, 1]:
            image = GameLoader.LOADER["spr_block_2x1"]
        else:
            image = GameLoader.LOADER["spr_block_3x1"]

        image = pygame.transform.scale(image, (size[0] * SQUARE_SIZE + SHADOW_SIZE,
                                               size[1] * SQUARE_SIZE + SHADOW_SIZE))
        return image


class SlipBlock(GameObject):
    """
        This block have something special!
    """

    def __init__(self, position, size):
        super(SlipBlock, self).__init__(position)
        self._layer = Layer.block
        self._size = size
        if self._size[0] >= self._size[1]:
            self._type = TypeDirection.horizontal
        else:
            self._type = TypeDirection.vertical
        self._is_holding = False
        self._image = self.block_image(size)
        self._delta = 0
        self._moving = False
        self._speed = 3.5
        self.fill_matrix(1)
        self.xx, self.yy = (0, 0)
        self._limit = [BOARD_POSITION[0],
                       BOARD_POSITION[1],
                       BOARD_POSITION[0] + SQUARE_SIZE * BOARD_SIZE,
                       BOARD_POSITION[1] + SQUARE_SIZE * BOARD_SIZE
                       ]

    def fill_matrix(self, value):
        grid_pos = grid_position(self._position)
        for i in range(self._size[1]):
            for j in range(self._size[0]):
                Global.MATRIX[grid_pos[0] + i][grid_pos[1] + j] = value

    def bound(self):
        x1 = self._position[0]
        y1 = self._position[1]
        x2 = self._position[0] + self._size[0] * SQUARE_SIZE
        y2 = self._position[1] + self._size[1] * SQUARE_SIZE
        return x1, y1, x2, y2

    def is_below_mouse_position(self):
        m_x, m_y = pygame.mouse.get_pos()
        bound = list(self.bound())
        if bound[0] < m_x < bound[2] and bound[1] < m_y < bound[3]:
            return True
        return False

    def auto_align_to_grid(self):
        xx = BOARD_POSITION[0] + round((self._position[0] - BOARD_POSITION[0]) / float(SQUARE_SIZE)) * SQUARE_SIZE
        yy = BOARD_POSITION[1] + round((self._position[1] - BOARD_POSITION[1]) / float(SQUARE_SIZE)) * SQUARE_SIZE
        self._position[0] += (xx - self._position[0]) / 2.0
        self._position[1] += (yy - self._position[1]) / 2.0

        if math.fabs(xx - self._position[0]) < 3:
            self._position[0] = xx

        if math.fabs(yy - self._position[1]) < 3:
            self._position[1] = yy

    def calculate_limit(self):
        # Default limit
        self._limit = [BOARD_POSITION[0],
                       BOARD_POSITION[1],
                       BOARD_POSITION[0] + SQUARE_SIZE * BOARD_SIZE,
                       BOARD_POSITION[1] + SQUARE_SIZE * BOARD_SIZE
                       ]
        # left - top - right - down
        i, j = grid_position(self._position)
        if self._type == TypeDirection.vertical:
            while i > 0:
                i -= 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[1] = real_position((i + 1, j))[1]
                    break
            while i < BOARD_SIZE - 1:
                i += 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[3] = real_position((i, j))[1]
                    break
        else:
            while j > 0:
                j -= 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[0] = real_position((i, j + 1))[0]
                    break
            while j < BOARD_SIZE - 1:
                j += 1
                if Global.MATRIX[i, j] == 1:
                    self._limit[2] = real_position((i, j))[0]
                    break

    def limit_position(self):
        bound = list(self.bound())
        if bound[0] < self._limit[0]:
            self._position[0] = self._limit[0]
            self.set_holding(False)
        if bound[1] < self._limit[1]:
            self._position[1] = self._limit[1]
            self.set_holding(False)
        if bound[2] > self._limit[2]:
            self._position[0] = self._limit[2] - self._size[0] * SQUARE_SIZE
            self.set_holding(False)
        if bound[3] > self._limit[3]:
            self._position[1] = self._limit[3] - self._size[1] * SQUARE_SIZE
            self.set_holding(False)

    def set_holding(self, value):
        self._is_holding = value
        if self._is_holding:
            Global.OLD_MATRIX = Global.MATRIX.copy()
            self.fill_matrix(0)
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            self._moving = False
            self.fill_matrix(1)
            if not numpy.array_equal(Global.MATRIX, Global.OLD_MATRIX):
                GameController.matrix_changed = True
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if GameLoader.PDATA.play_sound:
                pygame.mixer.Sound.play(GameLoader.LOADER["block_placed"])

    def update(self):
        m_x, m_y = pygame.mouse.get_pos()

        # Check if mouse is holding this block
        if GameController.mouse_down and pygame.mouse.get_cursor() != pygame.cursors.broken_x:
            if self.is_below_mouse_position():
                if not self._is_holding:
                    self.set_holding(True)

        if GameController.mouse_up and self._is_holding:
            if not self._moving:
                self.set_holding(False)

        # Move
        if self._is_holding:
            if not self._moving:
                self.xx = m_x - GameController.old_mouse_position[0]
                self.yy = m_y - GameController.old_mouse_position[1]
                if self._size[0] == self._size[1]:
                    if math.fabs(self.xx) >= math.fabs(self.yy):
                        self._type = TypeDirection.horizontal
                    else:
                        self._type = TypeDirection.vertical
                    if self.xx != 0 or self.yy != 0:
                        self.calculate_limit()
                        self._moving = True
                elif self._type == TypeDirection.horizontal:
                    if self.xx != 0:
                        self.calculate_limit()
                        self._moving = True
                else:
                    if self.yy != 0:
                        self.calculate_limit()
                        self._moving = True
            if self._moving:
                if self._type == TypeDirection.horizontal:
                    self._position[0] += self._speed*BLOCK_MOVE_SPEED*sign(self.xx)*Global.delta_time*FPS
                else:
                    self._position[1] += self._speed*BLOCK_MOVE_SPEED*sign(self.yy)*Global.delta_time*FPS
        self.limit_position()

        # Auto align
        if not self._is_holding:
            self.auto_align_to_grid()

    @staticmethod
    def block_image(size):
        size = list(size)

        if size == [1, 1]:
            image = GameLoader.LOADER["spr_glass_block_1x1"]
        elif size == [1, 2]:
            image = GameLoader.LOADER["spr_glass_block_1x2"]
        elif size == [1, 3]:
            image = GameLoader.LOADER["spr_glass_block_1x3"]
        elif size == [2, 1]:
            image = GameLoader.LOADER["spr_glass_block_2x1"]
        else:
            image = GameLoader.LOADER["spr_glass_block_3x1"]

        image = pygame.transform.scale(image, (size[0] * SQUARE_SIZE + SHADOW_SIZE,
                                               size[1] * SQUARE_SIZE + SHADOW_SIZE))
        return image


class TargetBlock(GameObject):
    """
        To win, move this block out of screen
    """

    def __init__(self, position):
        super(TargetBlock, self).__init__(position)
        self._layer = Layer.block
        self._image = pygame.transform.scale(GameLoader.LOADER["spr_target_block"], (SQUARE_SIZE * 2 + SHADOW_SIZE,
                                                                                     SQUARE_SIZE + SHADOW_SIZE))
        self._is_holding = False
        self._size = [2, 1]
        self._delta = 0
        self.fill_matrix(1)
        self._limit = [BOARD_POSITION[0],
                       BOARD_POSITION[0] + SQUARE_SIZE * (BOARD_SIZE + self._size[0] + 1)
                       ]

    def fill_matrix(self, value):
        grid_pos = grid_position(self._position)
        for i in range(self._size[1]):
            for j in range(self._size[0]):
                if grid_pos[1] + j >= BOARD_SIZE:
                    return
                Global.MATRIX[grid_pos[0] + i][grid_pos[1] + j] = value

    def bound(self):
        x1 = self._position[0]
        y1 = self._position[1]
        x2 = self._position[0] + self._size[0] * SQUARE_SIZE
        y2 = self._position[1] + self._size[1] * SQUARE_SIZE
        return x1, y1, x2, y2

    def is_below_mouse_position(self):
        m_x, m_y = pygame.mouse.get_pos()
        bound = list(self.bound())
        if bound[0] < m_x < bound[2] and bound[1] < m_y < bound[3]:
            return True
        return False

    def auto_align_to_grid(self):
        xx = BOARD_POSITION[0] + round((self._position[0] - BOARD_POSITION[0]) / float(SQUARE_SIZE)) * SQUARE_SIZE
        self._position[0] += (xx - self._position[0]) / 2.0

        if math.fabs(xx - self._position[0]) < 3:
            self._position[0] = xx

    def calculate_limit(self):
        # Default limit
        self._limit = [BOARD_POSITION[0],
                       BOARD_POSITION[0] + SQUARE_SIZE * (BOARD_SIZE + self._size[0] + 1)
                       ]
        # left - right
        i, j = grid_position(self._position)
        while j > 0:
            j -= 1
            if Global.MATRIX[i, j] == 1:
                self._limit[0] = real_position((i, j + 1))[0]
                break
        while j < BOARD_SIZE - 1:
            j += 1
            if Global.MATRIX[i, j] == 1:
                self._limit[1] = real_position((i, j))[0]
                break

    def limit_position(self):
        bound = list(self.bound())
        if bound[0] < self._limit[0]:
            self._position[0] = self._limit[0]
        if bound[2] > self._limit[1]:
            self._position[0] = self._limit[1] - self._size[0] * SQUARE_SIZE

    def set_holding(self, value):
        self._is_holding = value
        if self._is_holding:
            Global.OLD_MATRIX = Global.MATRIX.copy()
            self.fill_matrix(0)
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            self.calculate_limit()
        else:
            self.fill_matrix(1)
            if not numpy.array_equal(Global.MATRIX, Global.OLD_MATRIX):
                GameController.matrix_changed = True
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            if GameLoader.PDATA.play_sound:
                pygame.mixer.Sound.play(GameLoader.LOADER["block_placed"])

    def check_winning(self):
        if self._position[0] >= BOARD_POSITION[0] + (BOARD_SIZE - self._size[0]) * SQUARE_SIZE \
                and Global.GAME_STATE == GameState.playing:
            self.set_holding(False)
            Global.GAME_STATE = GameState.winning
            if GameLoader.PDATA.play_sound:
                pygame.mixer.Sound.play(GameLoader.LOADER['win'])

        if Global.GAME_STATE == GameState.winning:
            self._position[0] += 15
            if self._position[0] >= BOARD_POSITION[0] + SQUARE_SIZE * (BOARD_SIZE + 1):
                Global.GAME_STATE = GameState.end

    def update(self):
        m_x, m_y = pygame.mouse.get_pos()

        # Check if mouse is holding this block
        if GameController.mouse_down and pygame.mouse.get_cursor() != pygame.cursors.broken_x:
            if self.is_below_mouse_position():
                self.set_holding(True)
                self._delta = self._position[0] - m_x

        if GameController.mouse_up and self._is_holding:
            self.set_holding(False)

        # Move
        if self._is_holding:
            self._position[0] += ((m_x + self._delta) - self._position[0]) / 10.0 * BLOCK_MOVE_SPEED
        self.limit_position()

        # Auto align
        if (not self._is_holding) and Global.GAME_STATE == GameState.playing:
            self.auto_align_to_grid()

        # Win condition
        self.check_winning()


class SteelBlock(GameObject):
    """
        This block can not move!
    """

    def __init__(self, position, size):
        super(SteelBlock, self).__init__(position)
        self._layer = Layer.block
        size = list(size)
        self._image = self.block_image(size)
        self._size = size
        self.fill_matrix(1)

    def fill_matrix(self, value):
        grid_pos = grid_position(self._position)
        for i in range(self._size[1]):
            for j in range(self._size[0]):
                if grid_pos[1] + j >= BOARD_SIZE:
                    return
                Global.MATRIX[grid_pos[0] + i][grid_pos[1] + j] = value

    def bound(self):
        x1 = self._position[0]
        y1 = self._position[1]
        x2 = self._position[0] + self._size[0] * SQUARE_SIZE
        y2 = self._position[1] + self._size[1] * SQUARE_SIZE
        return x1, y1, x2, y2

    def is_below_mouse_position(self):
        m_x, m_y = pygame.mouse.get_pos()
        bound = list(self.bound())
        if bound[0] < m_x < bound[2] and bound[1] < m_y < bound[3]:
            return True
        return False

    def update(self):
        if GameController.mouse_down and self.is_below_mouse_position():
            pygame.mixer.Sound.play(GameLoader.LOADER["ignore"])

    @staticmethod
    def block_image(size):
        size = list(size)

        if size == [1, 1]:
            image = GameLoader.LOADER["spr_steel_block_1x1"]
        elif size == [1, 2]:
            image = GameLoader.LOADER["spr_steel_block_1x2"]
        elif size == [1, 3]:
            image = GameLoader.LOADER["spr_steel_block_1x3"]
        elif size == [2, 1]:
            image = GameLoader.LOADER["spr_steel_block_2x1"]
        else:
            image = GameLoader.LOADER["spr_steel_block_3x1"]

        image = pygame.transform.scale(image, (size[0] * SQUARE_SIZE + SHADOW_SIZE,
                                               size[1] * SQUARE_SIZE + SHADOW_SIZE))
        return image

from script.Entity import *
import Global


class LevelController:
    LEVEL_DATA: list[list[list[int]]] = []

    def __init__(self, row, column):
        self.ui = None
        self.lvl_select = None
        self.level = 1
        self.row = row
        self.column = column
        self.load_data()
        self.board = Board(BOARD_POSITION)
        self.border = Border((BOARD_POSITION[0] - 35, BOARD_POSITION[1] - 35))
        self.hide_board()

    def update(self):
        if Global.GAME_STATE == GameState.end:
            self.increase_level(1)

    def hide_board(self):
        self.board.set_active(False)
        self.border.set_active(False)

    def increase_level(self, i):
        self.level += i

        GameController.clear_layer(Layer.block)
        Global.GAME_STATE = GameState.playing

        if self.level > Global.MAX_LEVEL:
            self.level = Global.MAX_LEVEL
            self.ui.set_active(False)
            self.lvl_select.set_active(True)
            self.hide_board()
            return

        if self.level > GameLoader.PDATA.level_reached:
            GameLoader.PDATA.level_reached = self.level

        self.load_level(self.level)

    def restart_level(self):
        GameController.clear_layer(Layer.block)
        Global.GAME_STATE = GameState.playing
        self.load_level(self.level)

    def load_level(self, level):
        GameLoader.save_game()
        self.board.set_active(True)
        self.border.set_active(True)
        self.ui.set_active(True)
        self.level = level
        Global.MATRIX = numpy.zeros((self.row, self.column))
        list_block = self.LEVEL_DATA[level-1]
        # print(list_block)
        for block in list_block:
            if block[0] == TypeBlock.target.value:
                TargetBlock(real_position((block[1], block[2])))
            elif block[0] == TypeBlock.normal.value:
                WoodBlock(real_position((block[1], block[2])), (block[3], block[4]))
            elif block[0] == TypeBlock.slip.value:
                SlipBlock(real_position((block[1], block[2])), (block[3], block[4]))
            else:
                SteelBlock(real_position((block[1], block[2])), (block[3], block[4]))

    def load_data(self):
        with open("level/data.txt") as data:
            Global.MAX_LEVEL = int(next(data))
            for i in range(Global.MAX_LEVEL):
                n = int(next(data))
                list_block = []
                for j in range(n):
                    line = next(data)
                    list_block.append([int(x) for x in line.split()])
                self.LEVEL_DATA.append(list_block)
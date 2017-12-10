from application import *
from block import *
from random import random
import datetime
import tkinter as tk


class Game:
    WIDTH = 4
    LAST_SCORE_FILE = 'last_score.txt'

    def __init__(self, app, mode):
        self.grid = [[None for _ in range(4)] for _ in range(4)]
        self.app = app
        self.playing = True
        self.score = 0
        self.mode = mode
        self.values = self.generate_values()
        self.blocks_and_locations = self.generate_blocks_and_locations()

        self.create_next_block()
        self.draw_grid()

    def create_next_block(self):
        self.open_indices = self.get_open_indices()
        try:
            block, location = next(self.blocks_and_locations)
            self.grid[location[0]][location[1]] = block
        except IndexError:
            pass
        except StopIteration:
            self.locations = self.generate_locations()
        finally:
            if not self.has_move():
                self.app.lose_game()

    def has_move(self):
        if None in [j for i in self.grid for j in i]:
            return True
        for i, col in enumerate(self.grid):
            for j, block in enumerate(col):
                if not block or (self.grid[i][j] and
                   (self.can_merge_up(i, j) or self.can_merge_down(i, j) or
                   self.can_merge_left(i, j) or self.can_merge_right(i, j))):
                    return True
        return False

    def can_merge_up(self, col_num, row_num):
        return row_num > 0 and self.grid[col_num][row_num-1] and \
            self.grid[col_num][row_num-1].value == \
            self.grid[col_num][row_num].value

    def can_merge_down(self, col_num, row_num):
        return row_num < Game.WIDTH-1 and self.grid[col_num][row_num+1] and \
            self.grid[col_num][row_num+1].value == \
            self.grid[col_num][row_num].value

    def can_merge_left(self, col_num, row_num):
        return col_num > 0 and self.grid[col_num-1][row_num] and \
            self.grid[col_num-1][row_num].value == \
            self.grid[col_num][row_num].value

    def can_merge_right(self, col_num, row_num):
        return col_num < Game.WIDTH-1 and self.grid[col_num+1][row_num] and \
            self.grid[col_num+1][row_num].value == \
            self.grid[col_num][row_num].value

    def generate_blocks_and_locations(self):
        while self.playing:
            yield Block(next(self.values), self.mode), \
            	self.open_indices[int(random() * len(self.open_indices))]

    def get_open_indices(self):
        return [(i, j) for i, row in enumerate(self.grid)
                for j, _ in enumerate(row) if not self.grid[i][j]]

    def generate_values(self):
        while True:
            if self.mode == 'addition':
                yield 2 if random() < 0.85 else 4
            else:
                yield 65536 if random() < 0.9 else 256

    def reset(self):
        self.grid = list()
        self.draw_grid()

    def draw_grid(self):
        for i, row in enumerate(self.grid):
            for j, block in enumerate(row):
                color = self.get_color(block)
                i_left, i_right = self.get_border_dims(i)
                j_left, j_right = self.get_border_dims(j)

                self.app.game_canvas.create_rectangle(i_left, j_left,
                                                      i_right, j_right,
                                                      fill=color)
                if block:
                    self.write_number_on_block(block, i_left, i_right,
                                               j_left, j_right)

    def write_number_on_block(self, block, i_left, i_right, j_left, j_right):
        i_middle, j_middle = (i_left + i_right) / 2, (j_left + j_right) / 2

        self.app.game_canvas.create_text(i_middle, j_middle, text=block.value,
                                         fill=block.text_color)

    def read_high_scores(self):
        try:
            with open(Game.LAST_SCORE_FILE) as f:
                self.high_scores = f.read().split(',')
                return self.high_scores[0], self.high_scores[1]
        except OSError:
            return ''

    def write_high_score(self):
        date = str(datetime.date.today()).split('-')
        try:
            with open(Game.LAST_SCORE_FILE, 'w') as f:
                f.write(str(self.score) + ',' + '/'.join(date[1:] + [date[0]]))
        except OSError as e:
            return

    @staticmethod
    def get_border_dims(indx):
        return indx * Block.SIZE + Application.BORDER_SIZE, \
            (indx + 1) * Block.SIZE + Application.BORDER_SIZE

    @staticmethod
    def get_color(block):
        if block:
            return block.color
        else:
            return 'white'

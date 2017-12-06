# Started out with 'minimal application' provided in tkinter docs
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/minimal-app.html

import tkinter as tk
import tkinter.messagebox as tkmb
from random import random
import math
from game import *


class Application(tk.Frame):
    BORDER_SIZE = 5
    CANVAS_SIZE = 256 + BORDER_SIZE

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.start_game()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.resetButton = tk.Button(self, text='Reset',
                                     command=self.start_game)
        self.suggestionButton = tk.Button(self, text='My Best Move',
                                          command=suggest_move)
        self.game_canvas = self.create_game_canvas()
        self.status = tk.Label(self, text="Playing...")

        self.quitButton.grid()
        self.resetButton.grid()
        self.suggestionButton.grid()
        self.game_canvas.grid()
        self.status.grid()

    def start_game(self):
        self.game, self.status['text'] = Game(self), "Playing..."
        self.status.grid()

    def create_game_canvas(self):
        x_range = range(Application.BORDER_SIZE, Application.CANVAS_SIZE + 1)
        y_range = range(Application.BORDER_SIZE, Application.CANVAS_SIZE + 1)
        step = int((Application.CANVAS_SIZE - Application.BORDER_SIZE) /
                   Game.WIDTH)
        canvas = tk.Canvas(self, height=Application.CANVAS_SIZE,
                           width=Application.CANVAS_SIZE)
        for x in x_range[::step]:
            for y in y_range[::step]:
                canvas.create_rectangle(Application.BORDER_SIZE,
                                        Application.BORDER_SIZE, x, y)
        return canvas

    def get_canvas(self):
        return self.game_canvas

    def lose_game(self):
        self.status['text'] = "You've lost! Hit reset to play again."
        self.status.grid()


def suggest_move():
    move = get_max_empty_move([(get_max_empty('up'), 'up'), (get_max_empty('down'), 'down'), (get_max_empty('left'), 'left'), (get_max_empty('right'), 'right')])
                
    if len(move) > 2:
        move_options = ', '.join(move[:-2]) + ', ' + ', or '.join(move[-2:])
        tkmb.showinfo('Hint', 'Your best moves are ' + move_options)
    elif len(move) == 2:
        move_options = move[0] + ' or ' + move[1]
        tkmb.showinfo('Hint', 'Your best moves are ' + move_options)
    else:
        tkmb.showinfo('Hint', 'Your best move is ' + move[0])

def get_max_empty(dir):
    if dir == 'up':
        return max(count_empty(shift_blocks_up(shift_blocks_up(app.game.grid))),
            count_empty(shift_blocks_down(shift_blocks_up(app.game.grid))),
            count_empty(shift_blocks_right(shift_blocks_up(app.game.grid))),
            count_empty(shift_blocks_left(shift_blocks_up(app.game.grid))))
    elif dir == 'down':
        return max(count_empty(shift_blocks_up(shift_blocks_down(app.game.grid))),
            count_empty(shift_blocks_down(shift_blocks_down(app.game.grid))),
            count_empty(shift_blocks_right(shift_blocks_down(app.game.grid))),
            count_empty(shift_blocks_left(shift_blocks_down(app.game.grid))))
    elif dir == 'right':
        return max(count_empty(shift_blocks_up(shift_blocks_right(app.game.grid))),
            count_empty(shift_blocks_down(shift_blocks_right(app.game.grid))),
            count_empty(shift_blocks_right(shift_blocks_right(app.game.grid))),
            count_empty(shift_blocks_left(shift_blocks_right(app.game.grid))))
    elif dir == 'left':
        return max(count_empty(shift_blocks_up(shift_blocks_left(app.game.grid))),
            count_empty(shift_blocks_down(shift_blocks_left(app.game.grid))),
            count_empty(shift_blocks_right(shift_blocks_left(app.game.grid))),
            count_empty(shift_blocks_left(shift_blocks_left(app.game.grid))))

def count_empty(grid):
    count = 0
    for col in grid:
        for block in col:
            count += int(not bool(block))
    return count


def get_max_empty_move(nums_to_moves):
    most_empty = 0
    move_with_most_empty = ['up']
    for num_empty, move in nums_to_moves:
        if num_empty > most_empty:
            move_with_most_empty = [move]
            most_empty = num_empty
        elif num_empty == most_empty:
            move_with_most_empty += [move]
    return move_with_most_empty


def move_blocks_up(event):
    app.game.grid = shift_blocks_up(app.game.grid)
    put_block_in_grid()


def move_blocks_down(event):
    app.game.grid = shift_blocks_down(app.game.grid)
    put_block_in_grid()


def move_blocks_right(event):
    app.game.grid = shift_blocks_right(app.game.grid)
    put_block_in_grid()


def move_blocks_left(event):
    app.game.grid = shift_blocks_left(app.game.grid)
    put_block_in_grid()


def shift_blocks_down(grid):
    return [get_new_col(col[::-1])[::-1] for col in grid]


def shift_blocks_up(grid):
    return [get_new_col(col) for col in grid]


def get_new_col(col):
    new_col, have_merged = list(), False
    for block in col:
        if can_merge_vert(have_merged, block, new_col):
            new_col[-1] += block
            have_merged = True
        elif block:
            new_col.append(block)
    return new_col + [None for _ in range(Game.WIDTH - len(new_col))]


def can_merge_vert(have_merged, block, col):
    return block and not have_merged and len(col) > 0 \
           and col[-1].value == block.value


def shift_blocks_right(grid):
    return shift_horiz(grid, -1, -1, Game.WIDTH - 1)


def shift_blocks_left(grid):
    return shift_horiz(grid, 1, 1, 0)


def shift_horiz(grid, step, delta, first_col):
    new_grid = [[None for _ in range(Game.WIDTH)] for _ in range(Game.WIDTH)]
    for i in range(Game.WIDTH):
        new_grid = update_grid_for_row(new_grid, i,
                                       get_blocks_in_row(grid, i)[::step],
                                       delta, first_col)
    return new_grid


def get_blocks_in_row(grid, row_num):
    return [grid[i][row_num] for i in range(4) if grid[i][row_num]]


def update_grid_for_row(new_grid, row_num, blocks_in_row, delta, first_col):
    next_col, have_merged = first_col, False
    for i, block in enumerate(blocks_in_row):
        if can_merge_horiz(have_merged, new_grid, block,
                           next_col, row_num, delta, i):
            new_grid[next_col - delta][row_num] += block
            have_merged = True
        else:
            new_grid[next_col][row_num] = block
            next_col += delta
    return new_grid


def can_merge_horiz(have_merged, new_grid, block, col_num, row_num, delta, i):
    return not have_merged and is_in_bounds_after_movement(delta, col_num, i) \
        and new_grid[col_num - delta][row_num].value == block.value


def is_in_bounds_after_movement(delta, col_num, i):
    return (delta == 1 and i > 0) or (delta == -1 and col_num < Game.WIDTH - 1)


def put_block_in_grid():
    app.game.create_next_block()
    app.game.draw_grid()


if __name__ == '__main__':
    app = Application()
    app.master.title('2048')
    app.bind_all('<Key-Down>', move_blocks_down)
    app.bind_all('<Key-Up>', move_blocks_up)
    app.bind_all('<Key-Left>', move_blocks_left)
    app.bind_all('<Key-Right>', move_blocks_right)
    app.mainloop()

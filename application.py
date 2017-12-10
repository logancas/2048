# Started out with 'minimal application' provided in tkinter docs
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/minimal-app.html

import tkinter as tk
import tkinter.messagebox as tkmb
from random import random
from game import *


class Application(tk.Frame):
    BORDER_SIZE = 5
    CANVAS_SIZE = 360 + BORDER_SIZE
    INSTRUCTIONS_FILE = 'instructions.txt'

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.mode = 'addition'
        self.pack()
        self.create_widgets()
        self.start_game()
        self.previous_grid = self.game.grid

    def create_widgets(self):
        self.undo_button = tk.Button(self, text='Undo Last Move',
                                     command=self.undo)
        self.quit_button = tk.Button(self, text='Quit', command=self.quit)
        self.reset_button = tk.Button(self, text='Reset', command=self.reset)
        self.suggestion_button = tk.Button(self, text='My Best Move',
                                           command=self.suggest_move)

        self.instructions_button = tk.Button(self, text='Instructions',
                                             command=self.get_instructions)
        self.addition_mode_button = tk.Button(self, text='Addition Mode',
                                              command=self.addition_mode)
        self.sqrt_mode_button = tk.Button(self, text='Square Root Mode',
                                          command=self.sqrt_mode)

        self.game_canvas = self.create_game_canvas()
        self.score_canvas = tk.Canvas(self, height=Application.CANVAS_SIZE,
                                      width=128)
        self.score_header_label = tk.Label(self.score_canvas, text='Score: ')
        self.score_label = tk.Label(self.score_canvas, text='0')
        self.high_scores_header_label = tk.Label(self.score_canvas,
                                                 text='Last Score: ')
        self.high_scores_label = tk.Label(self.score_canvas, text='')
        self.date_header_label = tk.Label(self.score_canvas, text='Date:')
        self.date_label = tk.Label(self.score_canvas, text='')
        self.status = tk.Label(self, text="Playing...")

        self.quit_button.grid(row=1, column=2)
        self.reset_button.grid(row=1, column=1)
        self.suggestion_button.grid(row=0, column=1)
        self.undo_button.grid(row=1, column=0)
        self.instructions_button.grid(row=0, column=0)
        self.game_canvas.grid(row=2, columnspan=3)
        self.status.grid(columnspan=5)

        self.score_canvas.grid(row=2, column=3, columnspan=2)
        self.score_header_label.grid(in_=self.score_canvas, row=3, column=3)
        self.score_label.grid(in_=self.score_canvas, row=3, column=4)
        self.high_scores_header_label.grid(in_=self.score_canvas, row=6,
                                           column=3)
        self.high_scores_label.grid(in_=self.score_canvas, row=6, column=4)
        self.date_header_label.grid(in_=self.score_canvas, row=7, column=3)
        self.date_label.grid(in_=self.score_canvas, row=7, column=4)
        self.addition_mode_button.grid(row=0, column=3)
        self.sqrt_mode_button.grid(row=1, column=4)

    def create_game_canvas(self):
        x_range = range(Application.BORDER_SIZE, Application.CANVAS_SIZE + 1)
        y_range = range(Application.BORDER_SIZE, Application.CANVAS_SIZE + 1)
        step = int((Application.CANVAS_SIZE - Application.BORDER_SIZE) /
                   Game.WIDTH)
        canvas = tk.Canvas(self, height=Application.CANVAS_SIZE,
                           width=Application.CANVAS_SIZE)
        for x, y in zip(x_range[::step], y_range[::step]):
                canvas.create_rectangle(Application.BORDER_SIZE,
                                        Application.BORDER_SIZE, x, y)
        return canvas

    def get_canvas(self):
        return self.game_canvas

    def start_game(self):
        self.game = Game(self, self.mode)
        self.status['text'] = "Playing..."
        score_date_text = self.game.read_high_scores()
        self.high_scores_label['text'] = score_date_text[0]
        self.date_label['text'] = score_date_text[1]
        self.status.grid()

    def lose_game(self):
        self.status['text'] = "You've lost! Hit reset to play again."
        self.status.grid()
        self.game.write_high_score()

    def reset(self):
        self.score_label['text'] = '0'
        self.game.write_high_score()
        self.start_game()

    def undo(self):
        self.game.grid = self.previous_grid
        self.game.draw_grid()

    @staticmethod
    def get_instructions():
        try:
            with open(Application.INSTRUCTIONS_FILE, 'r') as f:
                instructions = f.read()
                tkmb.showinfo('Instructions', instructions)
        except OSError as e:
            print(e)
            return

    @staticmethod
    def suggest_move():
        move = get_best_move([(get_max_empty('up'), 'up'),
                              (get_max_empty('down'), 'down'),
                              (get_max_empty('left'), 'left'),
                              (get_max_empty('right'), 'right')])

        if len(move) > 2:
            move_options = ', '.join(move[:-2]) + ', ' + \
                           ', or '.join(move[-2:])
            tkmb.showinfo('Hint', 'Your best moves are ' + move_options)
        elif len(move) == 2:
            tkmb.showinfo('Hint', 'Your best moves are ' + move[0] +
                          ' or ' + move[1])
        else:
            tkmb.showinfo('Hint', 'Your best move is ' + move[0])

    @staticmethod
    def get_max_empty(dir):
        if dir == 'up':
            return max(count_none(shift_up(shift_up(app.game.grid))),
                       count_none(shift_down(shift_up(app.game.grid))),
                       count_none(shift_right(shift_up(app.game.grid))),
                       count_none(shift_left(shift_up(app.game.grid))))
        elif dir == 'down':
            return max(count_none(shift_up(shift_down(app.game.grid))),
                       count_none(shift_down(shift_down(app.game.grid))),
                       count_none(shift_right(shift_down(app.game.grid))),
                       count_none(shift_left(shift_down(app.game.grid))))
        elif dir == 'right':
            return max(count_none(shift_up(shift_right(app.game.grid))),
                       count_none(shift_down(shift_right(app.game.grid))),
                       count_none(shift_right(shift_right(app.game.grid))),
                       count_none(shift_left(shift_right(app.game.grid))))
        elif dir == 'left':
            return max(count_none(shift_up(shift_left(app.game.grid))),
                       count_none(shift_down(shift_left(app.game.grid))),
                       count_none(shift_right(shift_left(app.game.grid))),
                       count_none(shift_left(shift_left(app.game.grid))))

    @staticmethod
    def count_none(grid):
        count = 0
        for col in grid:
            count += len(col[not col])
        return count

    @staticmethod
    def get_best_move(nums_to_moves):
        most_empty = 0
        move_with_most_empty = ['up']
        for num_empty, move in nums_to_moves:
            if num_empty > most_empty:
                move_with_most_empty = [move]
                most_empty = num_empty
            elif num_empty == most_empty:
                move_with_most_empty += [move]
        return move_with_most_empty

    def addition_mode(self):
        self.mode = 'addition'
        self.game.mode = 'addition'
        self.reset()

    def sqrt_mode(self):
        self.mode = 'sqrt'
        self.game.mode = 'sqrt'
        self.reset()
        self.mode = 'sqrt'
        self.game.mode = 'sqrt'

    def move_blocks_up(self, event):
        self.update_grid(self.shift_up(self.game.grid))

    def move_blocks_down(self, event):
        self.update_grid(self.shift_down(self.game.grid))

    def move_blocks_right(self, event):
        self.update_grid(self.shift_right(self.game.grid))

    def move_blocks_left(self, event):
        self.update_grid(self.shift_left(self.game.grid))

    def update_grid(self, new_grid):
        if not new_grid == self.game.grid:
            self.previous_grid = self.game.grid
            self.game.grid = new_grid
            self.put_block_in_grid()

    def shift_down(self, grid):
        return [self.get_shifted_col(col[::-1])[::-1] for col in grid]

    def shift_up(self, grid):
        return [self.get_shifted_col(col) for col in grid]

    def get_shifted_col(self, col):
        new_col, have_merged = list(), False
        for block in col:
            if self.can_merge_vert(have_merged, block, new_col):
                new_col[-1] += block
                have_merged = True
                self.game.score += 12 * block.value
            elif block:
                new_col.append(block)
        return new_col + [None for _ in range(Game.WIDTH - len(new_col))]

    def can_merge_vert(self, have_merged, block, col):
        return block and not have_merged and len(col) > 0 \
               and col[-1].value == block.value

    def shift_right(self, grid):
        return self.shift_horiz(grid, -1, -1, Game.WIDTH - 1)

    def shift_left(self, grid):
        return self.shift_horiz(grid, 1, 1, 0)

    def shift_horiz(self, grid, step, delta, first_col):
        new_grid = [[None for _ in range(Game.WIDTH)]
                    for _ in range(Game.WIDTH)]
        for i in range(Game.WIDTH):
            new_grid = self.shift_row(new_grid, i,
                                      self.get_blocks_in_row(grid, i)[::step],
                                      delta, first_col)
        return new_grid

    def get_blocks_in_row(self, grid, row_num):
        return [grid[i][row_num] for i in range(4) if grid[i][row_num]]

    def shift_row(self, new_grid, row_num, blocks_in_row, delta, first_col):
        have_merged = False
        next_col = first_col
        for i, block in enumerate(blocks_in_row):
            if self.can_merge_horiz(have_merged, new_grid, block,
                                    next_col, row_num, delta, i):
                new_grid[next_col - delta][row_num] += block
                have_merged = True
                app.game.score += 12 * block.value
            else:
                new_grid[next_col][row_num] = block
                next_col += delta
        return new_grid

    def can_merge_horiz(self, have_merged, new_grid, block, col_num, row_num,
                        delta, i):
        return not have_merged and \
            self.is_in_bounds_after_move(delta, col_num, i) and \
            new_grid[col_num - delta][row_num].value == block.value

    @staticmethod
    def is_in_bounds_after_move(delta, col_num, i):
        return (delta == 1 and i > 0) or \
               (delta == -1 and col_num < Game.WIDTH - 1)

    def put_block_in_grid(self):
        self.game.create_next_block()
        self.game.draw_grid()
        self.score_label['text'] = self.game.score


if __name__ == '__main__':
    app = Application()
    app.master.title('2048')
    app.bind_all('<Key-Down>', app.move_blocks_down)
    app.bind_all('<Key-Up>', app.move_blocks_up)
    app.bind_all('<Key-Left>', app.move_blocks_left)
    app.bind_all('<Key-Right>', app.move_blocks_right)
    app.mainloop()

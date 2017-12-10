from application import *
from block import *
from random import random
import datetime
import tkinter as tk

class Game:
	WIDTH = 4
	LAST_SCORE_FILE = 'last_score.txt'

	def __init__(self, app):
		self.grid, self.app, self.playing, self.score = self.create_grid(), app, True, 0
		self.locations, self.values, self.blocks = self.generate_locations(), self.generate_values(), self.generate_blocks()
		self.create_next_block()
		self.draw_grid()		

	def create_grid(self):
		return [[None for _ in range(4)] for _ in range(4)]

	def create_next_block(self):
		self.available_coords = self.get_available_coords()
		try:
			location = next(self.locations)
			block = next(self.blocks)
			print(block.value)
			self.grid[location[0]][location[1]] = next(self.blocks)
		except IndexError:
			pass
		except StopIteration:
			self.locations = self.generate_locations()
		finally:
			if not self.has_move():
				self.app.lose_game()

	def has_move(self):
		for i, col in enumerate(self.grid):
			for j, block in enumerate(col):
				if not block or (self.grid[i][j] and (self.can_merge_up(i, j) or self.can_merge_down(i, j) or self.can_merge_left(i, j) or self.can_merge_right(i, j))):
					return True
		return False

	def can_merge_up(self, col_num, row_num):
		return row_num > 0 and self.grid[col_num][row_num-1] and self.grid[col_num][row_num-1].value == self.grid[col_num][row_num].value

	def can_merge_down(self, col_num, row_num):
		return row_num < Game.WIDTH-1 and self.grid[col_num][row_num+1] and self.grid[col_num][row_num+1].value == self.grid[col_num][row_num].value

	def can_merge_left(self, col_num, row_num):
		return col_num > 0 and self.grid[col_num-1][row_num] and self.grid[col_num-1][row_num].value == self.grid[col_num][row_num].value

	def can_merge_right(self, col_num, row_num):
		return col_num < Game.WIDTH-1 and self.grid[col_num+1][row_num] and self.grid[col_num+1][row_num].value == self.grid[col_num][row_num].value

	def generate_blocks(self):
		while self.playing:
<<<<<<< HEAD
			print('mode: ' + self.mode)
			yield Block(next(self.values), self.mode)
=======
			yield Block(next(self.values))
>>>>>>> parent of 027bf8f... Implemented additional mode.

	def generate_locations(self):
		while self.playing:
			yield self.available_coords[int(random() * len(self.available_coords))]

	def get_available_coords(self):
		return [tuple([i, j]) for i, row in enumerate(self.grid) for j, _ in enumerate(row) if not self.grid[i][j]]

	def generate_values(self):
		while True:
			yield 2 if random() < 0.85 else 4

	def reset(self):
		self.grid = list()
		self.draw_grid()

	def draw_grid(self):
		for i, row in enumerate(self.grid):
			for j, block in enumerate(row):
				color = get_color(block)
				i_left, i_right = get_border_dims(i)
				j_left, j_right = get_border_dims(j)

				self.app.game_canvas.create_rectangle(i_left, j_left, i_right, j_right, 
												 fill=color)
				if block:
					self.write_number_on_block(block, i_left, i_right, j_left, j_right)

	def write_number_on_block(self, block, i_left, i_right, j_left, j_right):
		i_middle = (i_left + i_right) / 2
		j_middle = (j_left + j_right) / 2

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

def get_border_dims(indx):
	return indx * Block.SIZE + Application.BORDER_SIZE, (indx + 1) * Block.SIZE  + Application.BORDER_SIZE
	
def get_color(block):
	if block:
		return block.color
	else:
		return 'white'

from application import *
import math

class Block:
	colors = {1: 'orange', 2: 'blue', 4: '#00ffff', 8: 'black', 16: 'green', 32: 'yellow', 64: 'brown', 128: 'orange', 256: 'red', 512: 'purple', 1024: 'white', 2048: 'grey'}
	text_colors = {1: 'white', 2: 'white', 4: 'black', 8: 'white', 16:'white', 32:'black', 64:'white', 128:'white', 256:'white', 512:'white', 1024:'black', 2048:'black'}
	SIZE = (Application.CANVAS_SIZE - Application.BORDER_SIZE) / 4

	def __init__(self, value, mode):
		self.value = value
		self.mode = mode
		while value > 2048:
			value = value / 2048
		self.color = Block.colors[value]
		self.text_color = Block.text_colors[value]
			
	def __add__(self, other):
		if self.mode == 'addition':
			return Block(self.value + other.value, self.mode)
		else:
			return Block(int(math.floor(math.sqrt(self.value))), self.mode)

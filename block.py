#Referenced this site for information on how to use colors in matlab
#https://matplotlib.org/examples/color/named_colors.html

from application import *
from matplotlib import colors as mcolors

class Block:
	colors = {2: 'blue', 4: '#00ffff', 8: 'black', 16: 'green', 32: 'yellow', 64: 'brown', 128: 'orange', 256: 'red', 512: 'purple', 1024: 'white', 2048: 'grey'}
	text_colors = {2: 'white', 4: 'black', 8: 'white', 16:'white', 32:'black', 64:'white', 128:'white', 256:'white', 512:'white', 1024:'black', 2048:'black'}
	SIZE = (Application.CANVAS_SIZE - Application.BORDER_SIZE) / 4

	def __init__(self, value):
		self.value = value
		self.color = Block.colors[value]
		self.text_color = Block.text_colors[value]

	def __add__(self, other):
		return Block(self.value + other.value)




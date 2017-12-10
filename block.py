from application import *
import math


class Block:
    colors = ['orange', 'blue', '#00ffff', 'black', 'green', 'yellow',
              'brown', 'orange', 'red', 'purple', 'white', 'grey']
    text_colors = ['white', 'white', 'black', 'white', 'white', 'black',
                   'white', 'white', 'white', 'white', 'black', 'black']
    SIZE = (Application.CANVAS_SIZE - Application.BORDER_SIZE) / 4

    def __init__(self, value, mode):
        self.value = value
        self.mode = mode
        value_in_range = self.get_value_in_range(value)
        self.color = Block.colors[int(math.log(value_in_range, 2))]
        self.text_color = Block.text_colors[int(math.log(value_in_range, 2))]

    @staticmethod
    def get_value_in_range(value):
        value_in_range = value
        while value_in_range > 2048:
            value_in_range = value_in_range / 2048
        return value_in_range

    def __add__(self, other):
        if self.mode == 'addition':
            return Block(self.value + other.value, self.mode)
        else:
            return Block(int(math.floor(math.sqrt(self.value))), self.mode)

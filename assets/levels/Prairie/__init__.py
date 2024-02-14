from modules import *
from ursina import *


config = {
    "description": "Dans la prairie, les vents murmurent des secrets à l'herbe",
    "difficulty": 1
}

def draw_board():
    models = ["cube" for _ in range(3)]
    level = Level(models=models)

    board = level.generate_board()
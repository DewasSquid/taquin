from modules import *
from ursina import *


config = {
    "name": "Prairie",
    "difficulty": 1
}

def draw_board():
    models = ["cube" for _ in range(3)]
    level = Level(models=models)

    board = level.generate_board()
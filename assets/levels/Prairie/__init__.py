from modules import *
from ursina import *


config = {
    "description": "Dans la prairie, les vents murmurent des secrets à l'herbe",
    "difficulty": 1
}

def main():
    models = ["cube" for _ in range(9)]
    level = Level(models=models)
    level.create()
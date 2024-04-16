from modules import *
from ursina import *

models = ["cube" for _ in range(25)]
level = Level(models=models)

config = {
    "description": "Dans les entrailles du volcan, la terre gronde et murmure ses mystères.",
    "difficulty": 3
}

def main():
    level.create()
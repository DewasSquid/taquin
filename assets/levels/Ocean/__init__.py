from modules import *
from ursina import *


config = {
    "description": "Dans l'océan infini, les vagues chuchotent des histoires au sable.",
    "difficulty": 2
}

def main():
    models = ["cube" for _ in range(16)]
    level = Level(models=models)
    level.create()
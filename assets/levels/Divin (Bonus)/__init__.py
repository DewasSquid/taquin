from modules import *
from ursina import *


config = {
    "description": "Au cœur du paradis, un gardien silencieux veille, son regard brûlant attend ceux qui osent défier l'éternité.",
    "difficulty": 8
}

def main():
    models = ["cube" for _ in range(36)]
    level = Level(models=models)
    level.create()
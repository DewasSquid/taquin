from modules import *
from ursina import *


models = ["cube" for _ in range(49)]
level = Level(models=models)

config = {
    "description": "Au cœur du paradis, un gardien silencieux veille, son regard brûlant attend ceux qui osent défier l'éternité.",
    "difficulty": 5
}

def main():
    level.create()
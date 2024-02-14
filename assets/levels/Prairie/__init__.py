from modules import *
from ursina import *


config = {
    "description": "Dans la prairie, les vents murmurent des secrets à l'herbe",
    "difficulty": 1
}

def main():
    models = ["cube" for _ in range(3)]
    level = Level(models=models)
    
    BackgroundImage(texture=Textures.MENU_BACKGROUND)

    board_seq = Sequence(
        Func(setattr, mouse, "enabled", False),
        Func(level.generate_board),
        Wait(2),
        Func(level.shuffle_board),
        Func(setattr, mouse, "enabled", True),
    )  # TODO: Convertir en fonction
    board_seq.start()
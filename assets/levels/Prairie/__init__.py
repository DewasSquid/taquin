from modules import *
from ursina import *


config = {
    "description": "Dans la prairie, les vents murmurent des secrets à l'herbe",
    "difficulty": 1
}

frame = GameFrame()

def disable_mouse():
    mouse.enabled = False

def enable_mouse():
    mouse.enabled = True

def main():
    models = ["cube" for _ in range(3)]
    level = Level(models=models)
    
    BackgroundImage(texture=Textures.MENU_BACKGROUND)

    board_seq = Sequence(
        Func(disable_mouse),
        Func(level.generate_board),
        Wait(2),
        Func(level.shuffle_board),
        Func(enable_mouse)
    )
    board_seq.start()
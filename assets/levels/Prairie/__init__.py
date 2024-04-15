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
    
    BackgroundImage(
        texture=Textures.MENU_BACKGROUND,
        scale=Vec2(level.model_amount**2, level.model_amount**window.aspect_ratio),
        position=Vec2(camera.position.x, camera.position.y)
    )
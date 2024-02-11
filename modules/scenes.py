import os

from ursina import *

from modules.custom_entities import *
from modules.visuals import *



class MainMenu(Scene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        camera.shader = Shaders.bloom()
        
        BackgroundImage(load_texture(Textures.MENU_BACKGROUND))

        Text(
            parent=camera.ui,
            text="Ijime No Game",
            scale=5,
            color=color.pink,
            position=Vec2(window.center.x - .4, window.center.y + .3),
        )

        menu_buttons = {
            "Jouer": Func(None),
            "Paramètres": Func(None),
            "Sortir": Func(quit)
        }

        for i, button in enumerate(menu_buttons.items()):
            text = button[0]
            command = button[1]

            Button(
                parent=camera.ui,
                text=text,
                scale=Vec2(.5,  .1),
                position=Vec2(window.center.x, window.center.y - (i * .15)),
                on_click=command
            )
from ursina import *
from modules.visuals import BackgroundImage


class Scene(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MainMenu(Scene):
    def __init__(self):
        BackgroundImage(load_texture("./assets/images/menu_bg"))

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
                position=Vec2(window.center.x, window.center.y + (i * -.15)),
                on_click=command
            )
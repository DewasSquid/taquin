from ursina import *
from modules.visuals import BackgroundImage, Textures


class Scene(Entity):
    def __init__(self, *args, **kwargs) -> None:
        """Instance de scène, une fois appelée, efface les éléments actuels."""
        super().__init__(*args, **kwargs)
        self.enabled = False

class MainMenu(Scene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
        BackgroundImage(load_texture(Textures.MENU_BACKGROUND))

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
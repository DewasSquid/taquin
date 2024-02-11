import os

from ursina import *

from modules.custom_entities import *
from modules.visuals import *


class Scene(Entity):
    def __init__(self, *args, **kwargs) -> None:
        """Instance de scène, une fois appelée, efface les éléments actuels."""
        super().__init__(*args, **kwargs)
        self.enabled = False

class Level(Scene):
    def __init__(self, level_path: str, *args, **kwargs) -> None:
        """Enregistre un niveau à partir d'une structure hiérarchisée précise

        Args:
            level_path (str): chemin d'accès à la structure hiérarchisée
        
        Examples:
        ```py
        GenerateLevel(level_path="./levels/level_perso")
        ```
        
        ```
        ./levels/level_perso
        |---> thumbnail.png
        |---> about.txt
        |---> ./assets/
              |---> fond.fichier_visuel
              |---> ./audio/
                    |---> fichiers_audio.wav
              |---> ./models/
                    |---> models_pour_les_cubes.obj
        """
        super().__init__(*args, **kwargs)
        self.__level_path = Path(level_path)
        self.data = self.__create_hierarchy(self.__level_path)

    def __create_hierarchy(self, path: str) -> dict:
        """Génère la liste des assets du niveau

        Args:
            path (str): Le chemin d'accès au dossier du niveau 

        Returns:
            dict: La liste des fichiers et sous-dossiers du niveau, automatiquement accédée par le jeu
        """
        data = {}
        for item in os.walk(path):
            pass

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
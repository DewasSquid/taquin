from ursina import *


class BackgroundImage(Entity):
    def __init__(self, texture : Texture, *args, **kwargs) -> None:
        """Entitée personnalisée permettant d'afficher une image de fond.
        Cette dernière s'étendra sur tout l'écran

        Args:
            texture (Texture): La texture a utiliser pour l'image
        """
        super().__init__(
            model="quad",
            texture=texture,
            scale=(window.size/100),
            z=1,
            *args,
            **kwargs
        )

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
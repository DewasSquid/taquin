from ursina import *
from pathlib import Path


class BackgroundImage(Entity):
    def __init__(self, texture : Texture, *args, **kwargs) -> None:
        """Entitée personnalisée permettant d"afficher une image de fond.
        Cette dernière s"étendra sur tout l"écran

        Args:
            texture (Texture): La texture a utiliser pour l"image
        """
        super().__init__(
            model="quad",
            texture=texture,
            scale=(window.size/100),
            z=1,
            *args,
            **kwargs
        )

class Level():
    def __init__(self, level_path: str, *args, **kwargs) -> None:
        """Enregistre un niveau à partir d"une structure hiérarchisée précise

        Args:
            level_path (str): chemin d"accès à la structure hiérarchisée
        """
        super().__init__(*args, **kwargs)
        self.__level_path = Path(level_path)
        self.data = self.__create_hierarchy(self.__level_path)

    def __create_hierarchy(self, path: Path) -> dict:
        """Crée une structure hiérarchisée à partir d"un chemin donné

        Args:
            path (Path): Chemin d"accès à la structure hiérarchisée

        Returns:
            dict: Structure hiérarchisée représentée en dictionnaire
        """
        hierarchy = {"name": path.name, "type": "folder", "children": []}

        for item in path.iterdir():
            if item.is_file():
                hierarchy["children"].append({"name": item.name, "type": "file"})
            elif item.is_dir():
                hierarchy["children"].append({"name": item.name, "type": "folder", "children": self.__create_hierarchy(item)})

        return hierarchy
from ursina import *


class Shaders:
    """Une énumération de shaders"""
    pass

class Textures:
    """Une énumération de chemin d'accès vers des textures"""
    MENU_BACKGROUND = "./assets/images/menu_bg.jpg"
    MENU_BG = MENU_BACKGROUND  # Alias

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
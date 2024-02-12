from ursina import *
from pathlib import Path


class BackgroundImage(Entity):
    def __init__(self, texture : Texture, *args, **kwargs) -> None:
        """Entitée personnalisée permettant d"afficher une image de fond.
        Cette dernière s"étendra sur tout l'écran

        Args:
            texture (Texture): La texture a utiliser pour l"image
        """
        super().__init__(
            model="quad",
            texture=texture,
            scale=(window.aspect_ratio, 1),
            color=color.white,
            world_y=-.15,
            z=1,
            *args,
            **kwargs
        )

class MenuButton(Button):
    def __init__(self, text: str, *arg, **kwargs) -> None:
        """Boutton personalisé avec style préfait

        Args:
            text (str): le texte à afficher
        """
        super().__init__(text, scale=(.25, .075), highlight_color=color.azure, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)
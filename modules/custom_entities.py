from ursina import *
from pathlib import Path


class BackgroundImage(Entity):
    def __init__(self, texture : Texture, opacity: int = 128, *args, **kwargs) -> None:
        """Entitée personnalisée permettant d"afficher une image de fond.
        Cette dernière s'étendra sur tout l'écran

        Args:
            texture (Texture): La texture a utiliser pour l"image
            opacity (float): Le pourcentage d'opacité de l'image. Plus élevé = plus opaque (0-255).
        """
        super().__init__(
            model="quad",
            texture=texture,
            scale=(window.aspect_ratio, 1),
            color=color.white,
            world_y=-.15,
            z=2,
            *args,
            **kwargs
        )
        
        # Une deuxième entitée au premier plan pour gérer l'opacité
        self._opacity = Entity(
            parent=self.parent,
            model="quad",
            scale=self.scale,
            color=color.rgba(0, 0, 0, opacity),
            world_y=self.world_y,
            z=1
        )
        
    @property
    def opacity(self) -> int:
        """Permet d'obtenir le niveau d'opacité de l'image"""
        return self._opacity.color.a
    
    @opacity.setter
    def opacity(self, value: int):
        """Permet de changer l'opacité de l'image

        Args:
            value (int): Le nouveau niveau d'opacité
        """
        self._opacity.color = color.rgba(0, 0, 0, value)

class MenuButton(Button):
    def __init__(self, text: str, *arg, **kwargs) -> None:
        """Boutton personalisé avec style préfait

        Args:
            text (str): le texte à afficher
        """
        super().__init__(text, scale=(.25, .075), highlight_color=color.azure, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)
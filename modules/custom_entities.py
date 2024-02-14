from ursina import *


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
    def __init__(self, text: str, tooltip: Tooltip = None, *arg, **kwargs) -> None:
        """Boutton personalisé avec style préfait

        Args:
            text (str): le texte à afficher
            tooltip (Tooltip): Une boite d'informations supplémentaires qui s's'affiche au passage de la souris
        """
        super().__init__(
            text=text,
            tooltip=tooltip,
            scale=(.25, .075),
            highlight_color=color.azure,
            *arg,
            **kwargs
        )

class Level(Entity):
    MIN_BRICKS = 3

    def __init__(self, models: list[Mesh], *args, **kwargs) -> None:
        """Structure pour un niveau de base
        
        Args:
            models (list[Mesh]): Une liste de tous les modèles de briques présents dans le niveau
        """
        super().__init__(*args, **kwargs)
        
        self.model_amount = len(models)
        if self.model_amount < self.MIN_BRICKS:
            raise Exception(f"Not enough brick models, the level needs to be at least {self.MIN_BRICKS}x{self.MIN_BRICKS}")
        
        self.models = models
        
        camera.position = Vec3(1, 1, (-1 * (self.model_amount**2)))

    def generate_board(self) -> list[list]:
        """Génère un tableau de taquin en fonction du nombre de modèles

        Returns:
            list: Une liste contenant chaque cube du tableau
        """
        i = 0
        row = []
        for x in range(self.model_amount):
            column = []
            for y, model in enumerate(self.models):
                i += 1
                brick = Entity(
                    model=model,
                    color=color.random_color(),
                    position=Vec3(x, y, 1),
                    scale=0
                )
                brick.animate_scale(value=1, duration=.1*i, curve=curve.out_circ)

                column.append(brick)
            row.append(column)
        return row

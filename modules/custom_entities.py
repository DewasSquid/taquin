from ursina import *
import random

class GameFrame(Entity):
    def __init__(self, *args, **kwargs):
        """Entitée "root", il est recommendé de l'utiliser en tant que parent"""
        super().__init__(
            parent=camera.ui,
            y=.15,
            *args,
            **kwargs
        )

class BackgroundImage(Entity):
    def __init__(self, texture : Texture, opacity: int = 128, *args, **kwargs) -> None:
        """Entitée personnalisée permettant d'afficher une image de fond.
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
            z=3,
            *args,
            **kwargs
        )
        
        # Une deuxième entitée au premier plan pour gérer l'opacité
        self._opacity = Entity(
            model="quad",
            scale=self.scale,
            color=color.rgba(0, 0, 0, opacity),
            z=2,
            *args,
            **kwargs
        )
        
    @property
    def opacity(self) -> int:
        """Permet d'obtenir le niveau d'opacité de l'image"""
        return self._opacity.color.a
    
    @opacity.setter
    def opacity(self, value: int) -> None:
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

class Brick(Button):
    def __init__(self, model: Mesh, id: int, level, *args, **kwargs) -> None:
        """Entitée représentant une brique de tableau

        Args:
            model (Mesh): Le modèle de la brique
            id (int): Son identifiant la représentant dans un tableau
            level (level): Le niveau parent
        """
        super().__init__(
            model=model,
            scale=0,
            *args,
            **kwargs
        )
        
        self.id = id
        self.level = level
        if self.id == 0:
            self.color = color.rgba(0, 0, 0, 0)
            self.highlight_color = self.color
            self.pressed_color = self.color

    def on_click(self) -> None:
        """Échange la position de cette brique avec la brique noire lorsqu'elle est cliquée"""
        if self == self.level.black_brick: return

        x1, y1, _ = self.position
        x2, y2, _ = self.level.black_brick.position

        if abs(x1 - x2) + abs(y1 - y2) == 1:
            self.level.swap_bricks(self, self.level.black_brick)
    
    def on_enable(self) -> None:
        """L'ors de l'affichage de la brique"""
        self.animate_scale(value=1, duration=.1*self.id, curve=curve.out_circ)

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
            raise Exception(f"The level has {self.model_amount} models but needs to be at least {self.MIN_BRICKS}x{self.MIN_BRICKS}")
        
        self.models = models
        self.black_brick = None
        
        self.setup_camera()
        
    def setup_camera(self) -> None:
        """Définie la position de la caméra en fonction du nombre de briques"""
        camera.position = Vec3(1, 1, (-1 * (self.model_amount**2)))
    
    @property
    def bricks(self) -> list[Brick]:
        """Renvoie une liste de toutes les briques présentes dans le niveau"""
        bricks = []
        for row in self.board:
            for brick in row:
                bricks.append(brick)
        return bricks

    def generate_board(self) -> None:
        """Génère un tableau de taquin en fonction du nombre de modèles"""
        i = 0
        row = []
        for x in range(self.model_amount):
            column = []
            for y, model in enumerate(self.models):
                brick = Brick(
                    parent=self.parent,
                    model=model,
                    color=color.random_color(),
                    id=i,
                    level=self,
                    position=Vec3(x, y, 1)
                )
                if brick.id == 0:
                    self.black_brick = brick
                column.append(brick)
                i += 1
            row.append(column)
        self.board = row

    def shuffle_board(self) -> None:
        """Mélange les briques du tableau"""
        bricks = self.bricks
        random.shuffle(bricks)
        
        # Réaffecte les briques mélangées au tableau
        for x, row in enumerate(self.board):
            for y, _ in enumerate(row):
                self.board[x][y] = bricks[x * len(row) + y]
                self.board[x][y].animate_position(value=Vec3(x, y, 1), duration=.2, curve=curve.linear)
    
    def swap_bricks(self, brick1: Brick, brick2: Brick) -> None:
        """Échange les positions de deux briques"""
        brick1_position, brick2_position = brick1.position, brick2.position
        brick1.animate_position(value=brick2_position, duration=.05, curve=curve.linear)
        brick2.animate_position(value=brick1_position, duration=.05, curve=curve.linear)
    
    def is_solved(self) -> bool:
        """Vérifie si le tableau est résolu"""
        i = 0
        for brick in self.bricks:
            if brick.id != i:
                return False
            i += 1
        return True
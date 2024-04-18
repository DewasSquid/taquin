import itertools
import math
import random

from ursina import *


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
            color=color.white,
            *args,
            **kwargs
        )
        
        self.id = id
        self.level = level
        
        if self.id == 0:
            self.color = color.rgba(0, 0, 0, 0)
            self.highlight_color = color.rgba(0, 0, 0, 0)
            return
        
        self.highlight_color = color.rgba(255, 0, 0, 100)
        
        self.id_text = Text(
            text=str(self.id),
            color=color.rgba(0, 0, 0, 0),
            scale=15,
            parent=self,
            origin=Vec3(-0.05, -0.05, 0),
            position=Vec3(0, 0, -1)
        )

    def on_click(self) -> None:
        """Échange la position de cette brique avec la brique noire lorsqu'elle est cliquée"""
        if self == self.level.black_brick: return

        x1, y1, _ = self.position
        x2, y2, _ = self.level.black_brick.position

        if abs(x1 - x2) + abs(y1 - y2) == 1:
            self.level.swap_bricks(self, self.level.black_brick)

class Level(Entity):
    MIN_BRICKS = 9
    
    def __init__(self, models: list[Mesh], *args, **kwargs) -> None:
        """Structure pour un niveau de base
        
        Args:
            models (list[Mesh]): Une liste de tous les modèles de briques présents dans le niveau
        """
        super().__init__(*args, **kwargs)
        
        self.model_amount = len(models)
        if self.model_amount < self.MIN_BRICKS:
            raise Exception(f"The level has {self.model_amount} models but needs to be at least {self.MIN_BRICKS}")
        
        self.dimension = math.ceil(math.sqrt(self.model_amount))
        
        self.models = models
        self.black_brick = None

    def setup_camera(self) -> None:
        """Définit la position de la caméra en fonction du nombre de briques"""
        # Merci à cet article qui m'as permis de trouver cette formule !
        # https://discourse.threejs.org/t/camera-zoom-to-fit-object/936
        
        scale_factor = max(1, self.model_amount / self.MIN_BRICKS)
        camera_distance = max(1, math.log(self.model_amount + 1, 2))
        min_camera_distance = 10
        camera_distance = max(camera_distance, min_camera_distance) * scale_factor

        grid_size = max(3, int(self.model_amount ** 0.5))
        center_x = (grid_size - 1) / 2
        center_y = (grid_size - 1) / 2

        camera.position = Vec3(center_x, center_y, -camera_distance)

    @property
    def bricks(self) -> list[Brick]:
        """Renvoie une liste de toutes les briques présentes dans le niveau"""
        bricks = []
        for row in self.board:
            for brick in row:
                bricks.append(brick)
        return bricks
    
    def create(self) -> None:
        """Séquence pour créé un niveau complet, avec tableau et séquence d'attente"""
        self.setup_camera()
        
        board_seq = Sequence(
            Func(setattr, mouse, "enabled", False),
            Func(self.generate_board),
            Wait(2.5),
            Func(self.shuffle_board),
            Wait(.5),
            Func(setattr, mouse, "enabled", True),
        )
        board_seq.start()

    def generate_board(self) -> None:
        """Génère un tableau de taquin en fonction du nombre de modèles"""
        column = []
        i = 0
        for x in range(self.dimension):
            row = []
            for y in range(self.dimension):
                model = self.models[i]
                
                brick = Brick(
                    parent=self.parent,
                    model=model,
                    id=i,
                    level=self,
                    position=Vec3(x, y, 1)
                )
                if brick.id == 0: self.black_brick = brick
                brick.animate_scale(
                    value=1,
                    duration=(brick.id/brick.level.model_amount)*1.5,
                    curve=curve.out_circ
                )
                if brick.id != 0:
                    brick.id_text.animate_color(
                        value=color.black,
                        duration=(brick.id/brick.level.model_amount)*1.5,
                        curve=curve.out_circ
                    )
                
                i += 1
                row.append(brick)
            column.append(row)
        self.board = column

    def shuffle_board(self) -> None:
        """Mélange les briques du tableau"""
        # Collecte les positions originales des briques dans la grille
        original_positions = {(brick.position.x, brick.position.y): brick for brick in self.bricks}
        
        # Génère un nouvel ordre aléatoire pour les positions des briques dans la grille
        random_positions = list(original_positions.keys())
        random.shuffle(random_positions)
        
        # Réaffecte les briques aux positions aléatoires dans la grille
        for (x1, y1), (x2, y2) in zip(original_positions.keys(), random_positions):
            original_positions[(x1, y1)].animate_position(Vec3(x2, y2, 1), duration=.15)
            self.board[int(x1)][int(y1)], self.board[int(x2)][int(y2)] = self.board[int(x2)][int(y2)], self.board[int(x1)][int(y1)]

    def swap_bricks(self, brick1: Brick, brick2: Brick) -> None:
        """Échange les positions de deux briques"""
        brick1_position, brick2_position = brick1.position, brick2.position
        brick1.animate_position(value=brick2_position, duration=.05, curve=curve.linear)
        brick2.animate_position(value=brick1_position, duration=.05, curve=curve.linear)

        x1, y1 = int(brick1_position.x), int(brick1_position.y)
        x2, y2 = int(brick2_position.x), int(brick2_position.y)
        self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]

        if not self.is_solved(): return
        WindowPanel(
            title="GAGNE !!",
            content=[Button(
                text="Retour",
                on_click=Func(os.execv, sys.executable, ['python'] + sys.argv)
            )],
            enabled=False
        )
    
    def is_solved(self) -> bool:
        """Vérifie si le tableau est résolu"""
        current_id = 0
        for row in self.board:
            for brick in row:
                if brick.id != current_id:
                    return False
                current_id += 1
        return True
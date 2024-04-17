import itertools
import math
import random
from typing import List
from ursina import *

class Brick(Button):
    def __init__(self, model: Mesh, id: int, level, *args, **kwargs) -> None:
        """Entity representing a brick in the board

        Args:
            model (Mesh): The model of the brick
            id (int): Unique identifier for the brick
            level (Level): The parent level
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
        """Swaps the position of this brick with the black brick when clicked"""
        if self == self.level.black_brick: return

        x1, y1, _ = self.position
        x2, y2, _ = self.level.black_brick.position

        if abs(x1 - x2) + abs(y1 - y2) == 1:
            self.level.swap_bricks(self, self.level.black_brick)

class Level(Entity):
    MIN_BRICKS = 9
    
    def __init__(self, models: List[Mesh], *args, **kwargs) -> None:
        """Structure for a basic level
        
        Args:
            models (List[Mesh]): List of all the brick models in the level
        """
        super().__init__(*args, **kwargs)
        
        self.model_amount = len(models)
        if self.model_amount < self.MIN_BRICKS:
            raise Exception(f"The level has {self.model_amount} models but needs to be at least {self.MIN_BRICKS}")
        
        self.dimension = math.ceil(math.sqrt(self.model_amount))
        
        self.models = models
        self._black_brick = None

    def setup_camera(self) -> None:
        """Sets camera position based on the number of bricks"""
        # Thanks to this article for the formula!
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
    def black_brick(self) -> Brick:
        """Returns the black brick"""
        return self._black_brick

    @black_brick.setter
    def black_brick(self, brick: Brick) -> None:
        """Sets the black brick"""
        self._black_brick = brick

    @property
    def bricks(self) -> List[Brick]:
        """Returns a list of all bricks in the level"""
        bricks = []
        for row in self.board:
            for brick in row:
                bricks.append(brick)
        return bricks
    
    @property
    def board(self) -> List[List[Brick]]:
        """Returns the current state of the game board"""
        board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        for row in range(self.dimension):
            for column in range(self.dimension):
                for brick in self.parent.children:
                    if brick.position.x == row and brick.position.y == column:
                        board[row][column] = brick
        return board 

    @board.setter
    def board(self, new_board: List[List[Brick]]) -> None:
        """Sets the state of the game board"""
        self._board = new_board

    def create(self) -> None:
        """Sequence to create a complete level, with board and wait sequence"""
        self.setup_camera()
        
        board_seq = Sequence(
            Func(setattr, mouse, "enabled", False),
            Func(self.generate_board),
            Wait(2),
            Func(self.shuffle_board),
            Wait(.5),
            Func(setattr, mouse, "enabled", True),
        )
        board_seq.start()

    def generate_board(self) -> None:
        """Generates a board based on the number of models"""
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
                    duration=(brick.id/brick.level.model_amount),
                    curve=curve.out_circ
                )
                
                i += 1
                row.append(brick)
            column.append(row)
        self.board = column

    def shuffle_board(self) -> None:
        """Shuffles the bricks on the board"""
        # Collect original positions of bricks on the grid
        original_positions = {(brick.position.x, brick.position.y): brick for brick in self.bricks}

        # Generate a new random order for brick positions on the grid
        random_positions = list(original_positions.keys())
        random.shuffle(random_positions)

        # Reassign bricks to random positions on the grid and update the board
        new_board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        for (x1, y1), (x2, y2) in zip(original_positions.keys(), random_positions):
            brick = original_positions[(x1, y1)]
            brick.animate_position(Vec3(x2, y2, 1), duration=.15)
            new_board[int(x2)][int(y2)] = brick

        self.board = new_board

    def swap_bricks(self, brick1: Brick, brick2: Brick) -> None:
        """Swaps the positions of two bricks"""
        brick1_position, brick2_position = brick1.position, brick2.position
        brick1.animate_position(value=brick2_position, duration=.05, curve=curve.linear)
        brick2.animate_position(value=brick1_position, duration=.05, curve=curve.linear)

        # Update the board immediately after swapping the bricks
        self._board = self.generate_board_state()

        print(self.is_solved())

    def generate_board_state(self) -> List[List[Brick]]:
        """Generates the current state of the game board"""
        board = [[None for _ in range(self.dimension)] for _ in range(self.dimension)]
        for row in range(self.dimension):
            for column in range(self.dimension):
                for brick in self.parent.children:
                    if brick.position.x == row and brick.position.y == column:
                        board[row][column] = brick
        return board

    def is_solved(self) -> bool:
        """Verifies if the board is solved"""
        flattened_board = [brick.id for row in self.board for brick in row if brick]
        for i, brick_id in enumerate(flattened_board):
            if brick_id != i:
                return False
        return True
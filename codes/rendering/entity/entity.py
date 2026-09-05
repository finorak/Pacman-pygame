from abc import ABC, abstractmethod
import pygame
from pygame.key import ScancodeWrapper

from codes.setting import CELL_SIZE

from ..component import AnimatedSprite


class Entity(ABC):
    UP = 0b0001
    RIGHT = 0b0010
    DOWN = 0b0100
    LEFT = 0b1000

    DIR_VEC = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0),
    }

    DIR_BIT = {
        "up": UP,
        "right": RIGHT,
        "down": DOWN,
        "left": LEFT,
    }

    OPPOSITE = {
        "up": "down",
        "down": "up",
        "left": "right",
        "right": "left",
    }

    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        self.grid_x: int = pos[0]
        self.grid_y: int = pos[1]
        self.render_x: float = float(pos[0])
        self.render_y: float = float(pos[1])

        self.maze = maze

        self.current_dir = "up"
        self.next_dir = "up"

        self.speed = 3.0
        self._move_buffer = 0.0
        self._is_moving = False
        self._move_progress = 0.0  # 0.0 to 1.0
        self._move_start = (self.grid_x, self.grid_y)
        self._move_target = (self.grid_x, self.grid_y)

        self.sprites = self.load_image()
        self.current_sprite = self.sprites[self.current_dir]
        self.current_sprite.position = (self.render_x, self.render_y)

    @abstractmethod
    def load_image(self) -> dict[str, AnimatedSprite]:
        """
        Loads the image for the sprite.

        The key for the sprite should always be "up", "down", "left", "right"
        to make the movement easier. We can also add another state as long as
        these keys is present.
        Returns:
            dict: The dictionnary containing the sprites.
        """

    @property
    def pos(self) -> tuple[int, int]:
        return self.grid_x, self.grid_y

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def can_move(self, direction: str) -> bool:
        dx, dy = self.DIR_VEC[direction]
        nx, ny = self.grid_x + dx, self.grid_y + dy

        if not self.in_bounds(self.grid_x, self.grid_y) or not self.in_bounds(
            nx, ny
        ):
            return False

        cur_mask = self.maze[self.grid_y][self.grid_x]

        if cur_mask == 15:
            return False

        out_bit = self.DIR_BIT[direction]

        return (cur_mask & out_bit) == 0

    @abstractmethod
    def get_input(self, key: ScancodeWrapper) -> None: ...

    def start_move(self, direction: str) -> None:
        dx, dy = self.DIR_VEC[direction]
        self.grid_x += dx
        self.grid_y += dy
        self.current_dir = direction
        self.current_sprite = self.sprites[direction]
        self._is_moving = True
        self._move_progress = 0.0
        self._move_start = (self.grid_x - dx, self.grid_y - dy)
        self._move_target = (self.grid_x, self.grid_y)

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)

        if self._is_moving:
            if (
                self.next_dir == self.OPPOSITE[self.current_dir]
                and self.next_dir != self.current_dir
            ):
                self.reverse_move(self.next_dir)
            self.move(dt)
        else:
            if self.can_move(self.next_dir):
                self.start_move(self.next_dir)
            elif self.can_move(self.current_dir):
                self.start_move(self.current_dir)

    def reverse_move(self, direction: str) -> None:
        old_start = self._move_start
        old_target = self._move_target

        self.grid_x, self.grid_y = old_start
        self.current_dir = direction
        self.current_sprite = self.sprites[direction]

        self._move_progress = 1.0 - self._move_progress
        self._move_start = old_target
        self._move_target = old_start
        self._is_moving = True

    def move(self, dt: float) -> None:
        self._move_progress += dt * self.speed
        if self._move_progress >= 1.0:
            self._move_progress = 1.0
            self._is_moving = False
        start_x, start_y = self._move_start
        target_x, target_y = self._move_target
        self.render_x = start_x + (target_x - start_x) * self._move_progress
        self.render_y = start_y + (target_y - start_y) * self._move_progress
        self.current_sprite.position = (self.render_x, self.render_y)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(
            self.current_sprite.image,
            (self.render_x * CELL_SIZE + 2, self.render_y * CELL_SIZE + 2),
        )

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Self

import pygame

from codes.rendering.component import AnimatedSprite
from codes.setting import (
    CELL_SIZE,
    DIR_BIT,
    DIR_VEC,
    OPPOSITE,
    PLAYER_PADDING,
)
from codes.utilities.utils import in_bounds, player_in_range


class Entity(ABC):
    ENTITY_STORE: ClassVar[list[Self]] = []

    def __init__(
            self, pos: tuple[int, int],
            maze: list[list[int]], life: int = 3
    ) -> None:
        self.grid_x = self.init_grid_x = pos[0]
        self.grid_y = self.init_grid_y = pos[1]
        self.render_x = self.init_render_x = float(pos[0])
        self.render_y = self.init_render_y = float(pos[1])
        self.life = life

        self.maze = maze

        self.current_dir = self.init_current_dir = "up"
        self.last_dir: str = self.current_dir
        self.next_dir = "up"

        self.speed = 3.0
        self._move_buffer = 0.0
        self._is_moving = False
        self._move_progress = 0.0  # 0.0 to 1.0
        self._move_start = self.init_move_start = (self.grid_x, self.grid_y)
        self._move_target = self._move_start

        self.sprites = self.load_image()
        self.current_sprite = self.init_current_sprite = self.sprites[
                self.current_dir]
        self.current_sprite.position = self.init_current_sprite_pos = (
                self.render_x, self.render_y)
        Entity.ENTITY_STORE.append(self)

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

    def can_move(self, direction: str) -> bool:
        dx, dy = DIR_VEC[direction]
        nx, ny = self.grid_x + dx, self.grid_y + dy

        if (
                not in_bounds(
                    self.grid_x, self.grid_y, self.maze
                    ) or not in_bounds(nx, ny, self.maze)
        ):
            return False
        # typechecking prevent mypy error.
        if (
                not TYPE_CHECKING
                and hasattr(self, "_cheat_mode")
                and self.cheat_mode
        ):
            return True

        cur_mask = self.maze[self.grid_y][self.grid_x]

        if cur_mask == 15:
            return False

        out_bit = DIR_BIT[direction]

        return (cur_mask & out_bit) == 0

    @abstractmethod
    def get_input(self, *arg: Any, **kwarg: Any) -> None | str: ...

    def start_move(self, direction: str) -> None:
        dx, dy = DIR_VEC[direction]
        self.grid_x += dx
        self.grid_y += dy
        self.current_dir = direction
        self._is_moving = True
        self.update_sprite(direction)
        self._move_progress = 0.0
        self._move_start = (self.grid_x - dx, self.grid_y - dy)
        self._move_target = (self.grid_x, self.grid_y)

    def update_sprite(self, sprite_name: str) -> None:
        self.current_sprite = self.sprites[sprite_name]

    def collides_with(self, other: "Entity") -> bool:
        return player_in_range(
                (self.render_x, self.render_y),
                (other.render_x, other.render_y),
                0.6)

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)

        if self._is_moving:
            if (
                self.next_dir == OPPOSITE[self.current_dir]
                and self.next_dir != self.current_dir
            ):
                self.reverse_move(self.next_dir)
            self.move(dt)
            return
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
            (
                self.render_x * CELL_SIZE + PLAYER_PADDING,
                self.render_y * CELL_SIZE + PLAYER_PADDING,
            ),
        )

    def _reset(self, kill: bool = False):
        if kill:
            self.life -= 1
        if hasattr(self, "can_be_eaten"):
            self.can_be_eaten = False
            self.start_timer = 0
        self.grid_x = self.init_grid_x
        self.grid_y = self.init_grid_y
        self.render_x = self.init_render_x
        self.render_y = self.init_render_y

        self.current_dir = self.init_current_dir

        self._move_buffer = 0.0
        self._is_moving = False
        self._move_progress = 0.0  # 0.0 to 1.0
        self._move_start = self.init_move_start
        self._move_target = self._move_start
        self.speed = 3.0

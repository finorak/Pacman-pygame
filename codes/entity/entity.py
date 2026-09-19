"""Entity module that contains the base of playe/ghost."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

import pygame

from codes.rendering.component import AnimatedSprite
from codes.setting import (
    CELL_SIZE,
    DIR_VEC,
    OPPOSITE,
    PLAYER_PADDING,
)
from codes.utilities import can_move, player_in_range


class Entity(ABC):
    """Entity class to manage player/ghost."""

    def __init__(
        self, pos: tuple[int, int], maze: list[list[int]], life: int = 3
    ) -> None:
        """Initialize an entity class instance.

        Args:
            pos: the current position of the entity.
            maze: the current maze.
            life: number of life the entity has.
        """
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
        self.speed = 3.5
        self.initial_speed = self.speed
        self._move_buffer = 0.0
        self._is_moving = False
        self._move_progress = 0.0  # 0.0 to 1.0
        self._move_start = self.init_move_start = (self.grid_x, self.grid_y)
        self._move_target = self._move_start

        self.sprites = self.load_image()
        self.current_sprite = self.init_current_sprite = self.sprites[
            self.current_dir
        ]
        self.current_sprite.position = self.init_current_sprite_pos = (
            self.render_x,
            self.render_y,
        )

    @abstractmethod
    def load_image(self) -> dict[str, AnimatedSprite]:
        """Load sprites images.

        The key for the sprite should always be "up", "down", "left", "right"
        to make the movement easier. We can also add another state as long as
        these keys is present.
        Returns:
            dict: The dictionnary containing the sprites.
        """

    @property
    def pos(self) -> tuple[int, int]:
        """Get entity position."""
        return self.grid_x, self.grid_y

    @abstractmethod
    def get_input(self, *arg: Any, **kwarg: Any) -> None | str:
        """Get input from user."""

    def start_move(self, direction: str) -> None:
        """Start move from current posiion to choosen direction.

        Args:
            direction: the direction choosen by the player, one of \
`up`, `down`, `left` and `right`
        """
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
        """Update entity sprite.

        Args:
            sprite_name: the name of the choosen sprite.
        """
        self.current_sprite = self.sprites[sprite_name]

    def collides_with(self, other: "Entity") -> bool:
        """Look for collision between two entity.

        Args:
            other: an other entity object.
        Returns:
            is_collide: the two entity do collide.
        """
        return player_in_range(
            (self.render_x, self.render_y),
            (other.render_x, other.render_y),
            0.6,
        )

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update current entity position and animation.

        Args:
            dt: delta time used so that the animation stays \
consistent even with other hardware.
        """
        self.current_sprite.animate(dt)
        cheat_mode: bool = False
        if hasattr(self, "_cheat_mode") and not TYPE_CHECKING:
            cheat_mode = self.cheat_mode

        if self._is_moving:
            if (
                self.next_dir == OPPOSITE[self.current_dir]
                and self.next_dir != self.current_dir
            ):
                self._reverse_move(self.next_dir)
            self._move(dt)
            return
        if can_move(*self.pos, self.next_dir, self.maze, cheat_mode):
            self.start_move(self.next_dir)
        elif can_move(*self.pos, self.current_dir, self.maze, cheat_mode):
            self.start_move(self.current_dir)

    def _reverse_move(self, direction: str) -> None:
        old_start = self._move_start
        old_target = self._move_target

        self.grid_x, self.grid_y = old_start
        self.current_dir = direction
        self.current_sprite = self.sprites[direction]

        self._move_progress = 1.0 - self._move_progress
        self._move_start = old_target
        self._move_target = old_start
        self._is_moving = True

    def _move(self, dt: float) -> None:
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
        """Render entity onto the screen.

        Args:
            screen: the surface to where to render the entity.
        """
        screen.blit(
            self.current_sprite.image,
            (
                self.render_x * CELL_SIZE + PLAYER_PADDING,
                self.render_y * CELL_SIZE + PLAYER_PADDING,
            ),
        )

    @abstractmethod
    def reset(self, kill: bool = False) -> None:
        """Reset the entity's information.

        Args:
            kill: wether diminue the entity's life or not.
        """
        if kill:
            self.life -= 1
        if hasattr(self, "can_be_eaten"):
            self.can_be_eaten = False
            self.start_timer = 0.0
        self.grid_x = self.init_grid_x
        self.grid_y = self.init_grid_y
        self.render_x = self.init_render_x
        self.render_y = self.init_render_y

        self.current_dir = "up"
        self.next_dir = "up"

        self._is_moving = False
        self._move_progress = 0.0  # 0.0 to 1.0
        self._move_start = self.init_move_start
        self._move_target = self._move_start
        self.speed = self.initial_speed

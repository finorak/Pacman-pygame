"""Ghost module to manage ghost."""

import random
from time import perf_counter
from typing import Any, ClassVar

import pygame
from mazegenerator import MazeGenerator

from codes.algorithm import Algorithm
from codes.rendering.component import AnimatedSprite
from codes.rendering.utils import SpriteLoader
from codes.setting import (
    DIR_VEC,
    GHOST_ESCAPE_TIME,
    RADIUS_UPGRAD_PER_LEVEL,
)
from codes.utilities import get_direction, player_in_range

from .entity import Entity


class Ghost(Entity):
    """Ghost class.

    The ghost inherit from entity so that we can
    focus on implementing the logic behind how the
    ghost behave.

    """

    GHOSTS_STORE: ClassVar[list["Ghost"]] = []

    def __init__(
        self,
        pos: tuple[int, int],
        maze: list[list[int]],
        name: str,
        score: int,
        maze_gen: MazeGenerator,
    ) -> None:
        """Initialize a ghost instance class.

        Args:
            pos: the position of the ghost.
            maze: current maze.
            name: name of the ghost.
            maze_gen: a `MazeGenerator` instance.
        """
        self.name = name
        super().__init__(pos, maze)
        self.speed = 2.0
        self.initial_speed = self.speed
        self.can_be_eaten: bool = False
        self.algorithm = Algorithm()
        self.start_timer: float = 0.0
        self.score: int = score
        self._radius: int = 4  # cell to count just upgrade as level grow
        self._target_position = pos
        self.maze_gen: MazeGenerator = maze_gen

        self.is_dead = False
        self.spawn_time = 0.0
        self.max_time = 2.0
        self.player_dead = False
        Ghost.GHOSTS_STORE.append(self)

    def load_image(self) -> dict[str, AnimatedSprite]:
        """Load sprites images.

        The key for the sprite should always be "up", "down", "left", "right"
        to make the movement easier. We can also add another state as long as
        these keys is present.
        Returns:
            dict: The dictionnary containing the sprites.
        """
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder(
                    "assets", "ghosts", self.name, direction
                ),
            )
        result["fragile"] = AnimatedSprite(
            (0, 0), SpriteLoader.import_folder("assets", "ghosts", "fragile")
        )
        result["fragile2"] = AnimatedSprite(
            (0, 0), SpriteLoader.import_folder("assets", "ghosts", "fragile2")
        )
        return result

    def update(self, dt: float) -> None:
        """Update entity sprite.

        Args:
            sprite_name: the name of the choosen sprite.
        """
        if self.player_dead:
            return
        if self.is_dead:
            self.spawn_time += dt
            if self.spawn_time > self.max_time:
                self.is_dead = False
                self.spawn_time = 0.0
                self.reset()
        # initialize timer
        if self.can_be_eaten and self.start_timer == 0:
            self.start_timer = perf_counter()
        # update timer
        if self.can_be_eaten:
            end = perf_counter()
            if (end - self.start_timer) + 3 >= GHOST_ESCAPE_TIME and (
                int((end - self.start_timer) * 3)
            ) % 2:
                self.update_sprite("fragile2")
            else:
                self.update_sprite("fragile")
            if end - self.start_timer >= GHOST_ESCAPE_TIME:
                self.can_be_eaten = False
                self.start_timer = 0
        super().update(dt)

    def _find_path(self, player: Any) -> str:
        """Find next path for ghost.

        The way we check for the next direction to be
        choosen by the ghost is very straitforward actualy.
        Given a 2 point (a, b) and (a', b') we search for
        the direction taken by the ghost and based on that
        we return the string representing that path.

        Args:
            player: Player instance, used to check the player's \
position.
        Returns:
            direction: string representing the direction, one of \
`up`, `down`, `left` and `right`
        """
        choices = ["down", "left", "right", "up"]
        next_dir = random.choice(choices)
        paths = self.algorithm.bfs(self.pos, player.pos, self.maze_gen)
        if self.can_be_eaten or player_in_range(
            self.pos, player.pos, self._radius
        ):
            if not paths:
                return self.next_dir
            next_dir = get_direction(paths[0], self.pos)
            choices.remove(next_dir)
            return random.choice(choices) if self.can_be_eaten else next_dir
        return next_dir

    def get_input(self, player: Any) -> None:
        """Get input from user.

        Args:
            player: the player
        """
        if self.is_dead:
            return
        self.player_dead = player.is_dead
        if self.player_dead:
            return
        if self.collides_with(player):
            if self.can_be_eaten:
                player.score += self.score
                self.start_timer = 0
                self.can_be_eaten = False
                self.is_dead = True
            else:
                Ghost.update_ghost_state(False)
                if not player.cheat_mode:
                    player.dead()
        if self._is_moving:
            return
        self.next_dir = self._find_path(player)

    def start_move(self, direction: str) -> None:
        """Start move from current posiion to choosen direction.

        Args:
            direction: the direction choosen by the player, one of
            `up`, `down`, `left` and `right`
        """
        dx, dy = DIR_VEC[direction]
        self.grid_x += dx
        self.grid_y += dy
        self.current_dir = direction
        self._is_moving = True
        self.update_sprite("fragile" if self.can_be_eaten else direction)
        self._move_progress = 0.0
        self._move_start = (self.grid_x - dx, self.grid_y - dy)
        self._move_target = (self.grid_x, self.grid_y)

    @classmethod
    def level_update(cls: Any) -> None:
        """Update ghosts radius per level update."""
        for ghost in Ghost.GHOSTS_STORE:
            ghost._radius += RADIUS_UPGRAD_PER_LEVEL

    @classmethod
    def update_ghost_state(cls: Any, value: bool = False) -> None:
        """Update ghosts state after each reset.

        Args:
            value: the state for each ghost after updating
            the default value is `False`
        """
        for ghost in Ghost.GHOSTS_STORE:
            ghost.start_timer = 0
            ghost.can_be_eaten = value
            if ghost.can_be_eaten:
                ghost.speed = 1.5
                ghost.start_timer = 0
            else:
                ghost.speed = ghost.initial_speed

    def reset(self, kill: bool = False) -> None:
        """Reset the entity's information.

        Args:
            kill: wether diminue the entity's life or not.
        """
        self.player_dead = False
        return super().reset(kill)

    def render(self, screen: pygame.Surface) -> None:
        """Render entity onto the screen.

        Args:
            screen: the surface to where to render the entity.
        """
        if self.is_dead:
            return
        return super().render(screen)

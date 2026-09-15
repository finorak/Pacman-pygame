import random
from time import perf_counter
from typing import Any, ClassVar

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
    GHOSTS_STORE: ClassVar[list["Ghost"]] = []

    def __init__(
        self,
        pos: tuple[int, int],
        maze: list[list[int]],
        name: str,
        score: int,
        maze_gen: MazeGenerator,
    ) -> None:
        self.name = name
        super().__init__(pos, maze)
        self.speed = 2.0
        self.initial_speed = self.speed
        self.can_be_eaten: bool = False
        self.algorithm = Algorithm()
        self.start_timer: float = 0.0
        self.score: int = score
        self._radius: int = 10  # cell to count just upgrade as level grow
        self._target_position = pos
        self.maze_gen: MazeGenerator = maze_gen
        Ghost.GHOSTS_STORE.append(self)

    def load_image(self) -> dict[str, AnimatedSprite]:
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
        return result

    def update(self, dt: float) -> None:
        # initialize timer
        if self.can_be_eaten and self.start_timer == 0:
            self.start_timer = perf_counter()
        # update timer
        if self.can_be_eaten:
            self.update_sprite("fragile")
            end = perf_counter()
            if end - self.start_timer >= GHOST_ESCAPE_TIME:
                self.can_be_eaten = False
                self.start_timer = 0
        super().update(dt)

    def _find_path(self, player: Any) -> str:
        choices = ["down", "left", "right", "up"]
        next_dir = random.choice(choices)
        paths = self.algorithm.bfs(self.pos, player.pos, self.maze_gen)
        if self.can_be_eaten:
            if not paths:
                return self.next_dir
            removed_dir = get_direction(paths[0], self.pos)
            choices.remove(removed_dir)
            return random.choice(choices)
        if player_in_range(self.pos, player.pos, self._radius):
            if not paths:
                return self.next_dir
            direction: str = get_direction(paths[0], self.pos)
            return direction
        return next_dir

    def get_input(self, player: Any) -> None:
        """This one will be used to change the target
        of the ghost.
        # player -> Player class
        """
        if self.collides_with(player):
            if player.cheat_mode:
                return
            if self.can_be_eaten:
                player.score += self.score
                self.can_be_eaten = False
                self.start_timer = 0
                self._reset()
            else:
                Ghost.update_ghost_state(False)
                player._reset(kill=True)
        if self._is_moving:
            return
        self.next_dir = self._find_path(player)

    def start_move(self, direction: str) -> None:
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
        for ghost in Ghost.GHOSTS_STORE:
            ghost._radius += RADIUS_UPGRAD_PER_LEVEL

    @classmethod
    def update_ghost_state(cls: Any, value: bool = False) -> None:
        for ghost in Ghost.GHOSTS_STORE:
            if not value:
                ghost.start_timer = 0
            ghost.can_be_eaten = value
            if ghost.can_be_eaten:
                ghost.speed = 1.0
            else:
                ghost.speed = ghost.initial_speed

import random
from time import perf_counter
from typing import Any, ClassVar

from codes.algorithm import Algorithm
from codes.rendering.component import AnimatedSprite
from codes.rendering.utils import SpriteLoader
from codes.setting import (
    GHOST_ESCAPE_TIME,
    RADIUS_UPGRAD_PER_LEVEL,
    TARGET_DIRECTION,
)
from codes.utilities import get_state, player_in_range

from .entity import Entity


class Ghost(Entity):
    GHOSTS_STORE: ClassVar = []
    def __init__(
        self, pos: tuple[int, int],
        maze: list[list[int]], name: str,
        score: int
    ) -> None:
        self.name = name
        super().__init__(pos, maze)
        self.speed = 2.0
        self.can_be_eaten: bool = False
        self.algorithm = Algorithm()
        self.start_timer: float = 0
        self.score: int = score
        self._radius: int = 2 # cell to count just upgrade as level grow
        self._target_position = pos
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
        return result

    def update(self, dt: float) -> None:
        # initialize timer
        if self.can_be_eaten and self.start_timer == 0:
            self.start_timer = perf_counter()
        # update timer
        if self.can_be_eaten:
            end = perf_counter()
            if end - self.start_timer >= GHOST_ESCAPE_TIME:
                self.can_be_eaten = False
                self.start_timer = 0
        super().update(dt)

    def _find_path(self, player: Any) -> str:
        # TODO: find why the ghost isn't moving
        # in the direction of the player even though
        # the algorithm seems right
        choices = ['down', 'left', 'right', 'up']
        next_dir = random.choice(choices)
        paths = self.algorithm.bfs(
                (
                    self.pos[0] - self.DIR_VEC[self.current_dir][0],
                    self.pos[1] - self.DIR_VEC[self.current_dir][1],
                 ),
                player.pos, self.maze)
        if self.can_be_eaten:
            if not paths:
                return self.next_dir
            target_vec = get_state(paths[0], self.pos)
            state = TARGET_DIRECTION[target_vec]
            choices.remove(state)
            return random.choice(choices)
        if (
                player_in_range(
                    (
                        self.pos[0] - self.DIR_VEC[self.current_dir][0],
                        self.pos[1] - self.DIR_VEC[self.current_dir][1]
                    ),
                    player.pos, self._radius)
        ):
            if not paths:
                return self.next_dir
            target_vec = get_state(paths[0], self.pos)
            state = TARGET_DIRECTION[target_vec]
            return state
        return next_dir

    def get_input(self, player: Any) -> None:
        """This one will be used to change the target
        of the ghost.
        # player -> Player class
        """
        if self._is_moving:
            return
        if self.pos == player.pos:
            if self.can_be_eaten:
                player.score += self.score
                self.can_be_eaten = False
                self.start_timer = 0
                self._reset()
            else:
                Ghost.update_ghost_state(False)
                player._reset(True)
        self.next_dir = self.OPPOSITE[self._find_path(player)]

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

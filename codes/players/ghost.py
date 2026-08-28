import math
import random
from typing import Any

from pygame import Surface

from codes.algorithm import Algorithm
from codes.setting import TARGET_DIRECTION
from codes.utilities import cell_is_valid, get_state

from .base import BasePlayer


class Ghost(BasePlayer):
    # When this is on, every
    # ghost can be eaten.
    CAN_BE_EATEN: bool = False

    def __init__(
            self, frames: dict[str, list[Surface]],
            pos: tuple[int, int], life: int
    ) -> None:
        super().__init__(frames, pos, life)
        self.speed = 120
        self._radius: int = 4
        # the target of the ghost
        self._target: tuple[int, int] = pos
        self.algorithm = Algorithm()

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def _is_in_range(self, player_pos: tuple[int, int]) -> bool:
        px, py = player_pos
        x = math.pow(px - self._x, 2)
        y = math.pow(py - self._y, 2)
        return (x + y) <= math.pow(self._radius, 2)

    def _target_reached(self) -> bool:
        return (self._x, self._y) == self._target

    def _find_path(
            self, current_pos: tuple[int, int],
            player_pos: tuple[int, int], 
            maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        return self.algorithm.bfs(current_pos, player_pos, maze)

    def _update_target(
            self, player_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> tuple[str, bool, tuple[int, int]]:
        if self._is_in_range(player_pos):
            paths = self._find_path(self.pos, player_pos, maze)
            if not paths:
                return self._state, False, self.pos
            new_state = get_state(paths[0], self.pos)
            return TARGET_DIRECTION[new_state], True, paths[0]
        target = random.choice([*TARGET_DIRECTION])
        dx, dy = target
        if not cell_is_valid(
                    (self._x, self._y),
                    (self._x + dx, self._y + dy),
                    maze
        ):
            return self._state, False, self.pos
        return (
                TARGET_DIRECTION[target],
                True,
                (self._x + dx, self._y + dy)
            )

    def update(
            self, dt: float, player_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> None:
        self.frame_update(dt)
        if self._target_reached():
            next_state, move_ghost, next_target = self._update_target(
                    player_pos, maze)
            if not move_ghost:
                return
            self._state = next_state
            self._target = next_target
        self._update_position(dt)

    def reset(self, *arg: Any, **kwarg: Any) -> None:
        ...

    # UPdate state of all ghost, to can('t) be eaten.
    @classmethod
    def update_ghost_state(cls: Any) -> 'Ghost':
        cls.CAN_BE_EATEN = not cls.CAN_BE_EATEN
        return cls

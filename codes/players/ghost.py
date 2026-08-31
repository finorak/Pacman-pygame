import random
from typing import Any

from pygame import Surface

from codes.algorithm import Algorithm
from codes.setting import TARGET_DIRECTION
from codes.utilities import (
    cell_is_valid,
    find_cell_neighboors,
    get_state,
    player_in_range,
    target_reached,
)

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
        self._radius: int = 3
        # the target of the ghost
        self._target: tuple[int, int] = pos
        self.algorithm = Algorithm()

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def _find_path(
            self, current_pos: tuple[int, int],
            player_pos: tuple[int, int], 
            maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        return self.algorithm.bfs(current_pos, player_pos, maze)

    def _escape_path(
            self, current_pos: tuple[int, int],
            player_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        paths = self.algorithm.bfs(current_pos, player_pos, maze)
        if not paths:
            return []
        forbiden_path = paths[0]
        current_cell_neighboors = find_cell_neighboors(maze, current_pos)
        return [cell for cell in current_cell_neighboors if cell != forbiden_path]

    def _update_target(
            self, player_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> tuple[str, bool, tuple[int, int]]:
        if self.CAN_BE_EATEN:
            paths = self._escape_path(self.pos, player_pos, maze)
            if not paths:
                return self._state, False, self.pos
            new_state = get_state(paths[0], self.pos)
            return TARGET_DIRECTION[new_state], True, paths[0]
        if player_in_range(self.pos, player_pos, self._radius):
            paths = self._find_path(self.pos, player_pos, maze)
            if not paths:
                return self._state, False, self.pos
            new_state = get_state(paths[0], self.pos)
            return TARGET_DIRECTION[new_state], True, paths[0]
        target = random.choice([*TARGET_DIRECTION])
        dx, dy = target
        if (
                not cell_is_valid(
                    (self._x, self._y),
                    (self._x + dx, self._y + dy),
                    maze
                    )
        ):
            return self._state, False, self.pos
        return (
                TARGET_DIRECTION[target],
                True,
                (self._x + dx, self._y + dy)
            )

    def update(
            self, dt: float, player: Any,
            maze: list[list[int]]
    ) -> None:
        """
        player -> Player instance
        """
        self.frame_update(dt)
        if target_reached(self.pos, self._target):
            next_state, move_ghost, next_target = self._update_target(
                    player.pos, maze)
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

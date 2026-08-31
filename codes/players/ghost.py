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
        self._target: list[int] = [0, 0]

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self._rect)

    def _cell_reached(self) -> bool:
        return [self.x, self.y] == self.target

    def update(self, dt: float, maze: list[list[int]]) -> None:
        # TODO: update this function because it start to
        # be full of random things
        self.base_update(dt)
        if self._cell_reached():
            directions = [-1, 0, 1]
            self.target = [
                random.choice(directions),
                random.choice(directions)
                ]
        if not self.cell_is_valid(
                (self.x, self.y),
                (
                    self.x + self.target[0],
                    self.y + self.target[1]
                ),
                maze
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

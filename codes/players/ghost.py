import random
from typing import Any

from pygame import Surface

from .base import BasePlayer


class Ghost(BasePlayer):
    def __init__(
            self,
            frames: dict[str, list[Surface]],
            pos: tuple[int, int],
            life: int
            ) -> None:
        super().__init__(frames, pos, life)
        self.speed = 130
        self.state = "right"
        # the target of the ghost
        self._target: list[int] = [0, 0]
        print(*self.target)

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
            print(self.target)
        if not self.cell_is_valid(
                (self.x, self.y),
                (
                    self.x + self.target[0],
                    self.y + self.target[1]
                ),
                maze
        ):
            return
        self._update_position(dt)

    def reset(self, *arg: Any, **kwarg: Any) -> None:
        ...

    @property
    def target(self) -> list[int]:
        return self._target

    @target.setter
    def target(self, value: list[int]) -> None:
        self._target = value

import random

from pygame import Surface

from .base import BasePlayer


class Ghost(BasePlayer):
    def __init__(
            self, frames: dict[str, list[Surface]], pos: tuple[int, int], life: int
            ) -> None:
        super().__init__(frames, pos, life)
        self._target: tuple[int, int] = (0, 0)

    def draw(self, screen: Surface) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    @property
    def target(self) -> tuple[int, int]:
        return self._target

    @target.setter
    def target(self, value: tuple[int, int]) -> None:
        self._target = value

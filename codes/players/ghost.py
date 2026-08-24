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
        self._target: tuple[int, int] = (0, 0)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self._rect)

    def update(self, dt: float, maze: list[list[int]]) -> None:
        self.base_update(dt)
        if not self.cell_is_valid((self.x, self.y), (self.x + 1, self.y + 1), maze):
            return
        self._update_position(dt)

    def reset(self, *arg: Any, **kwarg: Any) -> None:
        ...

    @property
    def target(self) -> tuple[int, int]:
        return self._target

    @target.setter
    def target(self, value: tuple[int, int]) -> None:
        self._target = value

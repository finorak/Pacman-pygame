from abc import ABC, abstractmethod
from typing import Any

import pygame
from pygame import Surface

from codes.setting import CELL_SIZE, DIRECTION_SETTING


class BasePlayer(ABC):
    def __init__(
            self,
            frames: dict[str, list[Surface]],
            pos: tuple[int, int],
            life: int,
    ) -> None:
        super().__init__()
        self._state: str = "right"
        self._frames = frames
        self._life = life
        self._x, self._y = pos
        self._frame_index: float = 0
        self.image = pygame.transform.scale(
                frames[self._state][0].convert_alpha(), (16, 16)
                ).convert_alpha()
        self.rect = frames[self._state][0].get_frect(topleft=(0, 0))
        self.speed: int = 140

    @abstractmethod
    def draw(self, screen: Surface) -> None: ...

    @abstractmethod
    def update(self, *arg: Any, **kwarg: Any) -> None: ...

    @abstractmethod
    def reset(self, *arg: Any, **kwarg: Any) -> None: ...

    def _update_position(self, dt: float) -> None:
        self.rect.x += self.speed * DIRECTION_SETTING[
                self._state]['x'] * dt
        self.rect.y += self.speed * DIRECTION_SETTING[
                self._state]['y'] * dt
        self._x = int(self.rect.x // CELL_SIZE)
        self._y = int(self.rect.y // CELL_SIZE)

    def frame_update(self, dt: float) -> None:
        self._frame_index += 7 * dt
        self.image = pygame.transform.scale(
                self._frames[self._state][
                    int(self._frame_index) % len(
                        self._frames[self._state]
                    )
                ].convert_alpha(), (16, 16)).convert_alpha()

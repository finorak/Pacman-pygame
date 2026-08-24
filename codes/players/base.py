from abc import ABC, abstractmethod
from typing import Any

import pygame
from pygame import Surface

from ..setting import CELL_SIZE, DIRECTION_SETTING


class BasePlayer(ABC):
    def __init__(
            self,
            frames: dict[str, list[Surface]],
            pos: tuple[int, int],
            life: int,
    ) -> None:
        super().__init__()
        self._state: str = "left"
        self._frames = frames
        self._life = life
        self._x, self._y = pos
        self._frame_index: float = 0
        self.image = pygame.transform.scale(
                frames[self._state][0].convert_alpha(), (16, 16)
                )
        self._rect = frames[self._state][0].get_frect(topleft=(0, 0))
        self.speed: int = 140

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        self._state = value

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def life(self) -> int:
        return self._life

    @life.setter
    def life(self, value: int) -> None:
        self.life = value

    @property
    def frame_index(self) -> float:
        return self._frame_index

    @frame_index.setter
    def frame_index(self, value: float) -> None:
        self._frame_index = value

    @abstractmethod
    def draw(self, screen: Surface) -> None: ...

    @abstractmethod
    def update(self, *arg: Any, **kwarg: Any) -> None: ...

    @abstractmethod
    def reset(self, *arg: Any, **kwarg: Any) -> None: ...

    def _update_position(self, dt: float) -> None:
        self._rect.x += self.speed * DIRECTION_SETTING[
                self.state]['x'] * dt
        self._rect.y += self.speed * DIRECTION_SETTING[
                self.state]['y'] * dt
        self.x = int(self._rect.x // CELL_SIZE)
        self.y = int(self._rect.y // CELL_SIZE)

    def base_update(self, dt: float) -> None:
        self.frame_index += 7 * dt
        self.image = pygame.transform.scale(
                self._frames[self.state][
                    int(self.frame_index) % len(
                        self._frames[self.state]
                    )
                ].convert_alpha(), (16, 16))

    def cell_is_valid(
            self,
            current_pos: tuple[int, int],
            new_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> bool:
        old_x, old_y = current_pos
        new_x, new_y = new_pos
        if (new_x < 0 or new_x >= len(maze)) \
                or (new_y < 0 or new_y >= len(maze[0])):
            return False
        return maze[old_x][old_y] & maze[new_x][new_y] != 0

from typing import Any

import pygame
from pygame import Surface

from codes.players.ghost import Ghost
from codes.setting import (
    DIRECTION_SETTING,
)
from codes.utilities import cell_is_valid

from .base import BasePlayer


class Player(BasePlayer):
    def __init__(
            self, frames: Any, pos: tuple[int, int], life: int
            ) -> None:
        super().__init__(frames, pos, life)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(
            self,
            dt: float,
            maze: list[list[int]]
    ) -> None:
        self.frame_update(dt)
        self.get_input(maze)
        if not self.get_input(maze):
            return
        self._update_position(dt)

    def reset(self, *arg: Any, **kwarg: Any) -> None:
        ...

    def get_input(self, maze: list[list[int]]) -> bool:
        keys = pygame.key.get_just_pressed()
        temp_state: str = self._state
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            temp_state = "down"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            temp_state = "up"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            temp_state = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            temp_state = "left"
        dx: int = DIRECTION_SETTING[temp_state]['x']
        dy: int = DIRECTION_SETTING[temp_state]['y']
        if cell_is_valid(
                (self._x, self._y),
                (self._x + dx, self._y + dy),
                maze
        ):
            self._state = temp_state
        return self._state == temp_state

    def update_ghost_state(self) -> None:
        Ghost.update_ghost_state()

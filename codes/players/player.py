from typing import Any

import pygame
from pygame import Surface

from ..setting import (
    DIRECTION_SETTING,
)
from .base import BasePlayer


class Player(BasePlayer):
    def __init__(
            self, frames: Any, pos: tuple[int, int], life: int
            ) -> None:
        super().__init__(frames, pos, life)
        self.state = "right"

    def draw(self, screen: Surface) -> None:
        # here, screen is the maze surface not the
        # main window/surface.
        screen.blit(self.image, self._rect)

    def update(
            self,
            dt: float,
            maze: list[list[int]]
    ) -> None:
        self.base_update(dt)
        self.get_input(maze)
        if not self.get_input(maze):
            return
        self._update_position(dt)

    def reset(self, *arg: Any, **kwarg: Any) -> None:
        ...

    def get_input(self, maze: list[list[int]]) -> bool:
        keys = pygame.key.get_just_pressed()
        self.state: str = self.state
        if keys[pygame.K_DOWN]:
            self.state = "down"
        elif keys[pygame.K_UP]:
            self.state = "up"
        elif keys[pygame.K_RIGHT]:
            self.state = "right"
        elif keys[pygame.K_LEFT]:
            self.state = "left"
        dx: int = DIRECTION_SETTING[self.state]['x']
        dy: int = DIRECTION_SETTING[self.state]['y']
        return self.cell_is_valid(
                (self.x, self.y),
                (self.x + dx, self.y + dy),
                maze
                )

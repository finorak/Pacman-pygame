from typing import Any

import pygame
from pygame import Surface

from .base import BasePlayer


class Player(BasePlayer):
    def __init__(
            self, frames: Any, pos: tuple[int, int], life: int
            ) -> None:
        super().__init__(frames, pos, life)

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self, dt: float) -> None:
        self.get_input()
        self.base_update(dt)

    def get_input(self) -> None:
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_DOWN]:
            self.state = "down"
        elif keys[pygame.K_UP]:
            self.state = "up"
        elif keys[pygame.K_RIGHT]:
            self.state = "right"
        elif keys[pygame.K_LEFT]:
            self.state = "left"

from typing import Any

from pygame import Surface
import pygame
from .base import BasePlayer
from ..setting import PLAYER_FRAME_SETTING


class Player(BasePlayer):
    def __init__(
            self, frames: Any, pos: tuple[int, int], life: int
            ) -> None:
        super().__init__(frames, pos, life)
        self.state: str = "left"
        self.player_rect = self.frames[self.state][
                self.current_frame_index
                ].get_rect(topleft=(0, 0))


    def draw(self, screen: Surface) -> None:
        screen.blit(
                self.frames[self.state][self.current_frame_index],
                self.player_rect
                )

    def update(self, dt: float) -> None:
        self.player_rect.x += PLAYER_FRAME_SETTING[self.state]['speed_x'] * dt
        self.player_rect.x += PLAYER_FRAME_SETTING[self.state]['speed_x'] * dt

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

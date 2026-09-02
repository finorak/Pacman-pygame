from abc import ABC, abstractmethod

import pygame

from ...setting import SCREEN_SIZE


class Screen(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.screen_size = SCREEN_SIZE

    @abstractmethod
    def get_input(self) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None: ...

    def get_center(self, lengh: float, horizontal: bool = True) -> int:
        if horizontal:
            return int((self.screen_size[0] - lengh) // 2)
        return int((self.screen_size[1] - lengh) // 2)


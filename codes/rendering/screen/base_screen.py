from abc import ABC, abstractmethod

import pygame


class Screen(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_input(self) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None: ...

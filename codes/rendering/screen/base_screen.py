from abc import ABC, abstractmethod

import pygame

from codes.parsing.parse import GameModel

from ...setting import SCREEN_SIZE
from ..utils import SpriteLoader


class Screen(ABC):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__()
        self.game_model = game_model
        self.screen_size = SCREEN_SIZE
        self.loader = SpriteLoader()

    @abstractmethod
    def get_input(self) -> str | None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None: ...

    def get_center(self, lengh: float, horizontal: bool = True) -> int:
        if horizontal:
            return int((self.screen_size[0] - lengh) // 2)
        return int((self.screen_size[1] - lengh) // 2)

    def __str__(self) -> str:
        return self.__class__.__name__.removesuffix("Screen")

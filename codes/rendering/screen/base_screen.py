"""Module that contains the base screen for the program."""

from abc import ABC, abstractmethod

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel

from ...setting import SCREEN_SIZE
from ..utils import SpriteLoader


class Screen(ABC):
    """The base screen for the rendering system."""

    def __init__(self, game_model: GameModel, data: Data) -> None:
        """
        Everything starts here.

        Args:
            game_model (GameModel): THe model or variable class for
            the program.
            data (Data): The data that stores every data used during
            the program.
        """
        super().__init__()
        self.data = data
        self.game_model = game_model
        self.screen_size = SCREEN_SIZE
        self.loader = SpriteLoader()

    @abstractmethod
    def get_input(self) -> str | None:
        """Get the input from the user."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and keys[pygame.K_LCTRL]:
            pygame.display.toggle_fullscreen()
        return None

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update the screen.

        Args:
            dt (float): The delta time.
        """

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """
        Render the screen into a surface.

        Args:
            screen (pygame.Surface): The surface to draw the program.
        """

    def get_center(self, lengh: float, horizontal: bool = True) -> int:
        """
        Get the center of the surface based on the lengh of the sprite.

        Args:
            lengh (float):The lengh of the sprite.
            horizontal (bool): horizontal or vertical position.
        Returns:
            int: The position of top or left.
        """
        if horizontal:
            return int((self.screen_size[0] - lengh) // 2)
        return int((self.screen_size[1] - lengh) // 2)

    def __str__(self) -> str:
        """Override to get the name of the program."""
        return self.__class__.__name__.removesuffix("Screen")

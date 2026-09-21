"""Module that contains the button class."""

import pygame

from codes.rendering.component.sprite import AnimatedSprite


class Button:
    """Class that represent a button in in a program."""

    def __init__(
        self,
        pos: tuple[int, int],
        sprites: dict[str, AnimatedSprite],
        result: str,
    ) -> None:
        """
        Everything starts here.

        Args:
            pos (tuple[int, int]): Position of the button in the screen.
            sprites (dict[str, AnimatedSprite]): The sprites of the button.
            This class need to have three state: normal, hover, pressed.
            result (str): The result of the string of the button (signal).
        """
        self.pos = pos
        self.sprites = sprites
        self.current_sprite = sprites["normal"]
        self.result = result

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button in the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        self.mouse_hover()
        screen.blit(self.current_sprite.image, self.pos)

    def mouse_hover(self) -> None:
        """Check if the mouse is in the button."""
        self.current_sprite = self.sprites["normal"]
        pos = pygame.mouse.get_pos()
        if self.current_sprite.rect.collidepoint(pos):
            self.current_sprite = self.sprites["hover"]

    def mouse_pressed(self) -> None:
        """Change the sprite of the button to be pressed."""
        self.current_sprite = self.sprites["pressed"]

    def call_back(self) -> str:
        """Return the result when we press the button."""
        return self.result

    def update(self, dt: float) -> None:
        """
        Update the button states.

        Args:
            dt (float): The delta time.
        """
        self.current_sprite.animate(dt)

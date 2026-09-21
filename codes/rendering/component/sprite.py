"""Module that contains the sprite and AnimatedSprite class."""

import pygame


class Sprite:
    """The sprite class for the program."""

    def __init__(
        self,
        pos: tuple[float, float],
        sprite: pygame.Surface,
    ) -> None:
        """
        Everything starts here.

        Args:
            pos (tuple[float, float]): the position of the sprite.
            sprite (pygame.Surface): The surface to be the sprite.
        """
        self.image = sprite
        self.rect = self.image.get_frect(topleft=pos)

    @property
    def position(self) -> tuple[float, float]:
        """
        Position of the sprite.

        Returns:
            tuple: The position in the screen.
        """
        return self.rect.topleft

    @position.setter
    def position(self, pos: tuple[float, float]) -> None:
        self.rect.topleft = pos


class AnimatedSprite(Sprite):
    """The animated sprite class for the program."""

    def __init__(
        self,
        pos: tuple[float, float],
        sprites: list[pygame.Surface],
    ) -> None:
        """
        Everything starts here.

        Args:
            pos (tuple[float, float]): The position of the sprite.
            sprites (list[pygame.Surface]): The list of surface to be
                the Animated sprite.
        """
        self.sprites = sprites
        self.sprite_index = 0.0
        self.animation_speed = 10
        self.sprite_count = len(self.sprites)
        super().__init__(pos, sprites[0])

    def animate(self, dt: float) -> None:
        """
        Animate the sprite.

        Args:
            dt (float): the deltatime.
        """
        self.sprite_index += dt * self.animation_speed
        self.image = self.sprites[int(self.sprite_index) % self.sprite_count]

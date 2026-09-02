"""
Here is my ideas on the pacman player.

First, the player should wander in the maze using index
Example:
the size of the maze is 32 * 32. The player position should go only
in 0 to 31 in both x and y

This is to make sure the player only go to the expected direction in the
expected time.
"""
import pygame

from .sprite import AnimatedSprite


class Player:
    def __init__(self, pos: tuple[int, int], sprites: dict[str, AnimatedSprite]) -> None:
        self.x = float(pos[0])
        self.y = float(pos[1])

        self.image = pygame.Surface((32, 32)).convert_alpha()
        self.rect = self.image.get_frect(center=(16, 16))

    def move(self, dt: float) -> None:
        # should be 3 cell per second
        self.x += 3 * dt

    def display(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

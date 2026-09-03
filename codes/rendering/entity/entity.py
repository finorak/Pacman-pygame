from abc import ABC
from enum import IntEnum

import pygame
from pygame.key import ScancodeWrapper

from codes.setting import CELL_SIZE

from ..component import AnimatedSprite


class Direction(IntEnum):
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class Entity(ABC):
    """
    Base Entity class for the player and ghost in the Maze.

    ...
    """

    def __init__(
        self,
        pos: tuple[int, int],
        sprites: dict[str, AnimatedSprite],
        maze: list[list[int]],
    ) -> None:
        # Store the direction and wanted direction
        self.direction: Direction = Direction.SOUTH
        self.next_direction: Direction = Direction.SOUTH

        # The position of the maze based on the tile and on the pixel
        self.tile_x, self.tile_y = pos
        self.pixel_x, self.pixel_y = (float(x) for x in pos)

        # The speed of the entity, Here is 3 cell per second.
        self.speed = 3

        # The actual maze
        self.maze = maze

        # the sprite in a dict format
        # The key must be always "up", "down", "left", "right"
        self.sprites = sprites

        # The current sprite for the animation.
        self.current_sprite = self.sprites["down"]

    def request_direction(self, direction: Direction) -> None:
        self.next_direction = direction

    def get_input(self, key: ScancodeWrapper) -> None:
        # Take the input of the user to the maze
        if key[pygame.K_w]:
            self.request_direction(Direction.NORTH)
        elif key[pygame.K_s]:
            self.request_direction(Direction.SOUTH)
        elif key[pygame.K_d]:
            self.request_direction(Direction.EAST)
        elif key[pygame.K_a]:
            self.request_direction(Direction.WEST)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(
            self.current_sprite.image,
            (
                self.pixel_x * CELL_SIZE + 3,
                self.pixel_y * CELL_SIZE + 3,
            ),
        )

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        if not (0 <= x < len(self.maze[0]) and 0 <= y < len(self.maze)):
            return False
        return not self.has_wall(x, y, direction)

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        return bool(self.maze[y][x] & direction)

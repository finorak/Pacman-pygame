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
from pygame.key import ScancodeWrapper

from codes.setting import CELL_SIZE

from ..utils import SpriteLoader
from .sprite import AnimatedSprite


class Player:

    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        self.current_dir = "up"
        self.next_dir = "up"

        self.x = float(pos[0])
        self.y = float(pos[1])

        self.maze = maze

        self.speed = 3

        self.sprites = self.load_image()
        self.current_sprite = self.sprites["up"]

        self.available_dir = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
        }

    def move(self, dt: float) -> None:
        # should be 3 cell per second
        dx, dy = self.available_dir[self.current_direction]
        if -0.1 <= round(self.x) % 1 <= 0.1 and -0.1 <= round(self.y) % 1 <= 0.1:
            print(self.x, self.y)
            if self.cell_is_valid(
                (int(self.x), int(self.y)),
                (int(self.x) + dx, int(self.y) + dy),
            ):
                self.pos = (
                    self.pos[0]
                    + self.available_dir[self.current_dir][0]
                    * dt
                    * self.speed,
                    self.pos[1]
                    + self.available_dir[self.current_dir][1]
                    * dt
                    * self.speed,
                )
            self.current_sprite.position = self.x, self.y
        else:
            self.pos = (
                self.pos[0]
                + self.available_dir[self.current_dir][0]
                * dt
                * self.speed,
                self.pos[1]
                + self.available_dir[self.current_dir][1]
                * dt
                * self.speed,
            )
        self.current_sprite.position = self.x, self.y

    def load_image(self) -> dict[str, AnimatedSprite]:
        directions = {"down", "left", "right", "up"}
        result = {}
        for direction in directions:
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder("assets", "pacman", direction),
            )
        return result

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)
        self.move(dt)

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, pos: tuple[float, float]) -> None:
        self.x, self.y = pos

    @property
    def current_direction(self) -> str:
        return self.current_dir

    @current_direction.setter
    def current_direction(self, dir: str) -> None:
        self.current_sprite = self.sprites[dir]
        self.current_sprite.position = self.x, self.y
        self.current_dir = dir

    def get_input(self, key: ScancodeWrapper) -> None:
        if key[pygame.K_w]:
            self.current_direction = "up"
        elif key[pygame.K_s]:
            self.current_direction = "down"
        elif key[pygame.K_d]:
            self.current_direction = "right"
        elif key[pygame.K_a]:
            self.current_direction = "left"

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(
            self.current_sprite.image,
            (
                self.current_sprite.rect.topleft[0] * CELL_SIZE,
                self.current_sprite.rect.topleft[1] * CELL_SIZE,
            ),
        )

    def cell_is_valid(
        self,
        current_pos: tuple[int, int],
        new_pos: tuple[int, int],
    ) -> bool:
        old_x, old_y = current_pos
        new_x, new_y = new_pos
        if (0 > old_y >= len(self.maze)) or (0 > old_x >= len(self.maze[0])):
            return False
        if (0 > new_y >= len(self.maze)) or (0 > new_x >= len(self.maze[0])):
            return False
        try:
            if self.maze[new_y][new_x] == 15:
                return False
            return self.maze[old_y][old_x] & self.maze[new_y][new_x] != 0
        except IndexError:
            return False

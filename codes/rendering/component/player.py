
import pygame
from pygame.key import ScancodeWrapper

from codes.setting import CELL_SIZE

from ..utils import SpriteLoader
from .sprite import AnimatedSprite


class Player:
    # wall/opening bits
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8

    DIR_VEC = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0),
    }

    DIR_BIT = {
        "up": UP,
        "right": RIGHT,
        "down": DOWN,
        "left": LEFT,
    }

    OPPOSITE = {
        "up": "down",
        "right": "left",
        "down": "up",
        "left": "right",
    }

    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        self.x = int(pos[0])  # grid index only
        self.y = int(pos[1])  # grid index only
        self.maze = maze

        self.current_dir = "up"
        self.next_dir = "up"

        self.speed = 3.0  # cells per second
        self._move_buffer = 0.0

        self.sprites = self.load_image()
        self.current_sprite = self.sprites[self.current_dir]
        self.current_sprite.position = (self.x, self.y)

    def load_image(self) -> dict[str, AnimatedSprite]:
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder("assets", "pacman", direction),
            )
        return result

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def can_move(self, direction: str) -> bool:
        dx, dy = self.DIR_VEC[direction]
        nx, ny = self.x + dx, self.y + dy

        if not self.in_bounds(self.x, self.y) or not self.in_bounds(nx, ny):
            return False

        cur_mask = self.maze[self.y][self.x]
        nxt_mask = self.maze[ny][nx]

        # Optional hard wall encoding
        if cur_mask == 15 or nxt_mask == 15:
            return False

        out_bit = self.DIR_BIT[direction]
        in_bit = self.DIR_BIT[self.OPPOSITE[direction]]

        # Both cells must NOT have walls in the passage direction
        return (cur_mask & out_bit) == 0 and (nxt_mask & in_bit) == 0

    def get_input(self, key: ScancodeWrapper) -> None:
        if key[pygame.K_w]:
            self.next_dir = "up"
        elif key[pygame.K_s]:
            self.next_dir = "down"
        elif key[pygame.K_d]:
            self.next_dir = "right"
        elif key[pygame.K_a]:
            self.next_dir = "left"

    def move_one_cell(self) -> None:
        # try buffered direction first
        if self.can_move(self.next_dir):
            self.current_dir = self.next_dir

        if not self.can_move(self.current_dir):
            return

        dx, dy = self.DIR_VEC[self.current_dir]
        self.x += dx
        self.y += dy
        self.current_sprite = self.sprites[self.current_dir]
        self.current_sprite.position = (self.x, self.y)

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)

        self._move_buffer += dt * self.speed
        while self._move_buffer >= 1.0:
            self.move_one_cell()
            self._move_buffer -= 1.0

    def render(self, screen: pygame.Surface) -> None:
        px = self.x * CELL_SIZE
        py = self.y * CELL_SIZE
        screen.blit(self.current_sprite.image, (px, py))


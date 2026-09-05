

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
        self.grid_x = int(pos[0])  # grid index
        self.grid_y = int(pos[1])  # grid index
        self.render_x = float(pos[0])  # render position
        self.render_y = float(pos[1])  # render position
        
        self.maze = maze

        self.current_dir = "up"
        self.next_dir = "up"

        self.speed = 3.0  # cells per second
        self._move_buffer = 0.0
        self._is_moving = False
        self._move_progress = 0.0  # 0.0 to 1.0
        self._move_start = (self.grid_x, self.grid_y)
        self._move_target = (self.grid_x, self.grid_y)

        self.sprites = self.load_image()
        self.current_sprite = self.sprites[self.current_dir]
        self.current_sprite.position = (self.render_x, self.render_y)

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
        return self.grid_x, self.grid_y

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def can_move(self, direction: str) -> bool:
        dx, dy = self.DIR_VEC[direction]
        nx, ny = self.grid_x + dx, self.grid_y + dy

        if not self.in_bounds(self.grid_x, self.grid_y) or not self.in_bounds(nx, ny):
            return False

        cur_mask = self.maze[self.grid_y][self.grid_x]
        nxt_mask = self.maze[ny][nx]

        if cur_mask == 15 or nxt_mask == 15:
            return False

        out_bit = self.DIR_BIT[direction]
        in_bit = self.DIR_BIT[self.OPPOSITE[direction]]

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

    def start_move(self, direction: str) -> None:
        dx, dy = self.DIR_VEC[direction]
        self.grid_x += dx
        self.grid_y += dy
        self.current_dir = direction
        self.current_sprite = self.sprites[direction]
        
        self._is_moving = True
        self._move_progress = 0.0
        self._move_start = (self.grid_x - dx, self.grid_y - dy)
        self._move_target = (self.grid_x, self.grid_y)

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)

        # Handle smooth movement
        if self._is_moving:
            self._move_progress += dt * self.speed
            if self._move_progress >= 1.0:
                self._move_progress = 1.0
                self._is_moving = False
            # Interpolate render position
            start_x, start_y = self._move_start
            target_x, target_y = self._move_target
            self.render_x = start_x + (target_x - start_x) * self._move_progress
            self.render_y = start_y + (target_y - start_y) * self._move_progress
            self.current_sprite.position = (self.render_x, self.render_y)
        else:
            # Queue next move
            if self.can_move(self.next_dir):
                self.start_move(self.next_dir)
            elif self.can_move(self.current_dir):
                self.start_move(self.current_dir)

    def render(self, screen: pygame.Surface) -> None:
        px = int(self.render_x * CELL_SIZE) + 2
        py = int(self.render_y * CELL_SIZE) + 2
        screen.blit(self.current_sprite.image, (px, py))



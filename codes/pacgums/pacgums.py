import random

import pygame

from ..rendering.utils import SpriteLoader
from ..setting import CELL_SIZE, GUM_PADDING


class Pacgums:
    def __init__(
        self, maze: list[list[int]], pacgum_score: int, super_pacgum_score: int
    ) -> None:
        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        self.pacgum_score = pacgum_score
        self.super_pacgum_score = super_pacgum_score

        self.maze = maze

        self.all_pos = self.get_all_pos()

        self.pacgum_image = SpriteLoader.import_image("assets", "other", "dot")
        self.super_pacgum_image = SpriteLoader.import_image(
            "assets", "other", "big_dot"
        )

    def render(self, screen: pygame.Surface) -> None:
        for pos in self.pacgums:
            screen.blit(
                self.pacgum_image,
                (
                    pos[0] * CELL_SIZE + GUM_PADDING,
                    pos[1] * CELL_SIZE + GUM_PADDING,
                ),
            )
        for pos in self.super_pacgums:
            screen.blit(
                self.super_pacgum_image,
                (
                    pos[0] * CELL_SIZE + GUM_PADDING,
                    pos[1] * CELL_SIZE + GUM_PADDING,
                ),
            )

    def generate_gums(self, numbers: int) -> None:
        self.pacgums.clear()
        self.super_pacgums.clear()

        for i in range(random.randint(1, 15)):
            random.shuffle(self.all_pos)

        self.pacgums = set(self.all_pos[:numbers])
        self.super_pacgums = {
            (0, 0),
            (len(self.maze) - 1, len(self.maze[0]) - 1),
            (0, len(self.maze[0]) - 1),
            (len(self.maze) - 1, 0),
        }

    def get_all_pos(self) -> list[tuple[int, int]]:
        all_pos = []
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] != 15:
                    all_pos.append((col, row))
        all_pos.remove((0, 0))
        all_pos.remove((len(self.maze[0]) - 1, len(self.maze) - 1))
        all_pos.remove((0, len(self.maze) - 1))
        all_pos.remove((len(self.maze[0]) - 1, 0))
        return all_pos

    def eat(self, pos: tuple[int, int]) -> int:
        if pos in self.pacgums:
            self.pacgums.remove(pos)
            return self.pacgum_score
        elif pos in self.super_pacgums:
            self.super_pacgums.remove(pos)
            return self.super_pacgum_score
        return 0

    def is_empty(self) -> bool:
        return not self.pacgums and not self.super_pacgums

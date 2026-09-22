"""Pacgums class management module."""

import random
import time

import pygame

from ..rendering.utils import SpriteLoader
from ..setting import CELL_SIZE, GUM_PADDING


class Pacgums:
    """Pacgum class manager."""

    def __init__(
        self,
        maze: list[list[int]],
        pacgum_score: int,
        super_pacgum_score: int,
    ) -> None:
        """
        Everything starts here.

        Args:
            maze (list[list[int]]): The maze for the pacgum.
            pacgum_score (int): The score for the pacgum.
            super_pacgum_score (int): The score for the super pacgum.
        """
        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        self.pacgum_score = pacgum_score
        self.super_pacgum_score = super_pacgum_score

        self.maze = maze

        self.all_pos = self._get_all_pos()

        self.pacgum_image = SpriteLoader.import_image("assets", "other", "dot")
        self.super_pacgum_image = SpriteLoader.import_image(
            "assets", "other", "big_dot"
        )

    def render(self, screen: pygame.Surface) -> None:
        """Render pacgum on the screen.

        Args:
            screen: where to place the pacgum on the screen.
        """
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
        """Generate pacgums.

        Args:
            numbers: how many pacgum to generate.
        """
        self.pacgums.clear()
        self.super_pacgums.clear()

        random.seed(time.time())
        positions = random.sample(self.all_pos, numbers)

        self.pacgums = set(positions[:numbers])
        self.super_pacgums = {
            (0, 0),
            (len(self.maze[0]) - 1, len(self.maze) - 1),
            (0, len(self.maze) - 1),
            (len(self.maze[0]) - 1, 0),
        }

    def _get_all_pos(self) -> list[tuple[int, int]]:
        """Get valid position to put the gum.

        Returns:
            positions: a list of tuple of position.
        """
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
        """Eat the gum from the position.

        Given a position, we try to eat the
        gum in it if there is any, we remove it from
        our dictionary so that it no longer be displayed.

        Args:
            pos: the position of the gum.
        Returns:
            the score of that gum.
        """
        if pos in self.pacgums:
            self.pacgums.remove(pos)
            return self.pacgum_score
        elif pos in self.super_pacgums:
            self.super_pacgums.remove(pos)
            return self.super_pacgum_score
        return 0

    @property
    def is_empty(self) -> bool:
        """Check for pacgums valability."""
        return not self.pacgums

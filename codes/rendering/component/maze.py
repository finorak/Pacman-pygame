"""Module that contains the base of the maze."""

import pygame
from mazegenerator import MazeGenerator

from codes.rendering.utils import SpriteLoader
from codes.setting import CELL_PADDING, CELL_SIZE


class Maze:
    """class that store The maze in the program and more."""

    def __init__(self, size: tuple[int, int], seed: int = 0) -> None:
        """
        Everything starts here.

        Args:
            size (tuple[int, int]): The size of the maze.
            seed (int): The seed to generate the maze.
        """
        self.maze_gen = MazeGenerator(size, seed=seed)
        self.maze = self.maze_gen.maze
        self.cell_size: int = CELL_SIZE
        self.maze_size = self._get_maze_size(self.maze)
        self.full_block = SpriteLoader.import_image(
            "assets", "other", "full_cell"
        )
        self.background = self._get_maze_surface()
        self.image = self.background.copy()
        self.rect: pygame.FRect = self.image.get_frect()
        self.width, self.height = size

    @property
    def size(self) -> tuple[int, int]:
        """
        The size of the maze.

        Returns:
            tuple: Value as a width, height tupple.
        """
        return self.width, self.height

    def _reset(self) -> None:
        """Reset the screen to be only the background."""
        self.image.fill((0, 0, 0, 30))
        self.image.blit(self.background)

    def _get_maze_surface(self) -> pygame.Surface:
        """
        Get The maze rendered as a surface.

        Returns:
            pygame: The surface that contains the maze.
        """
        surface = pygame.Surface(
            self.maze_size, pygame.SRCALPHA, 32
        ).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                if col == 15:
                    real_pos = x * self.cell_size + 1, y * self.cell_size + 1
                    surface.blit(self.full_block, (real_pos))
                    continue
                self._draw_cell(surface, (x, y), col)
        return surface

    def _get_maze_size(self, maze: list[list[int]]) -> tuple[int, int]:
        """
        Get the size of the maze.

        Args:
            maze (list[list[int]]): The maze.
        Returns:
            tuple: the surface size as a width, height tuple.
        """
        return (
            len(maze[0]) * self.cell_size + CELL_PADDING,
            len(maze) * self.cell_size + CELL_PADDING,
        )

    def _draw_cell(
        self, surface: pygame.Surface, pos: tuple[int, int], value: int
    ) -> None:
        """
        Draw a cell in a surface.

        Args:
            surface (pygame.Surface): The surface to draw the cell.
            pos (tuple[int, int]): The position of the cell.
            value (int): The value of the cell (0 - 15).
        """
        real_pos = pos[0] * self.cell_size + 1, pos[1] * self.cell_size + 1
        color = (50, 105, 50)
        i = 0
        while (value >> i) != 0:
            if ((value >> i) & 1) != 1:
                i += 1
                continue
            if i == 0:
                self._draw_line(
                    surface,
                    real_pos,
                    (real_pos[0] + self.cell_size, real_pos[1]),
                    color,
                )
            elif i == 1:
                self._draw_line(
                    surface,
                    (real_pos[0] + self.cell_size, real_pos[1]),
                    (
                        real_pos[0] + self.cell_size,
                        real_pos[1] + self.cell_size,
                    ),
                    color,
                )
            elif i == 2:
                self._draw_line(
                    surface,
                    (real_pos[0], real_pos[1] + self.cell_size),
                    (
                        real_pos[0] + self.cell_size,
                        real_pos[1] + self.cell_size,
                    ),
                    color,
                )
            else:
                self._draw_line(
                    surface,
                    (real_pos[0], real_pos[1]),
                    (real_pos[0], real_pos[1] + self.cell_size),
                    color,
                )
            i += 1

    def _draw_line(
        self,
        surface: pygame.Surface,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple[int, int, int],
        thickness: int = 2,
    ) -> None:
        """
        Draw a line in a surface.

        Args:
            surface (pygame.Surface): The surface to draw the cell.
            start (tuple[int, int]): The starting position of the line
            end (tuple[int, int]): The ending position of the line
            thickness (int): The thickness of the line. Default=2
        """
        x0, y0 = start
        x1, y1 = end

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy

        while True:
            for dx_thick in range(-thickness // 2, thickness // 2 + 1):
                for dy_thick in range(-thickness // 2, thickness // 2 + 1):
                    surface.set_at((x0 + dx_thick, y0 + dy_thick), color)

            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the maze in a surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        surface.blit(self.image, self.rect)
        self._reset()

    def reset(self, seed: int = 0) -> None:
        """
        Reset the maze screen.

        Args:
            seed (int): the seed of the maze.
        """
        self.maze_gen.generate(seed)
        self.maze = self.maze_gen.maze
        self._get_maze_surface()

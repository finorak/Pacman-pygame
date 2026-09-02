import pygame


class Maze:
    def __init__(self, maze: list[list[int]]) -> None:
        self.maze = maze
        self.cell_size: int = 35
        self.maze_size = self._get_maze_size(maze)
        self.background = self._get_maze_surface()
        self.image = self.background.copy()
        self.rect: pygame.FRect = self.image.get_frect(topleft=(100, 100))

    def reset(self) -> None:
        self.image.blit(self.background)

    def _get_maze_surface(self) -> pygame.Surface:
        surface = pygame.Surface(self.maze_size)
        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                self._draw_cell(surface, (x, y), col)
        return surface

    def _get_maze_size(self, maze: list[list[int]]) -> tuple[int, int]:
        return (len(maze[0]) * self.cell_size + 20+ 5, len(maze) * self.cell_size + 20)

    def _draw_cell(
        self, surface: pygame.Surface, pos: tuple[int, int], value: int
    ) -> None:
        real_pos = pos[0] * self.cell_size + 5, pos[1] * self.cell_size + 5
        color = (255, 255, 255)
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

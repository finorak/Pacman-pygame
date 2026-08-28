from collections import deque

from codes.setting import EAST, NORTH, SOUTH, WEST


class Algorithm:
    def __init__(self) -> None:
        pass

    def bfs(
            self,
            start_pos: tuple[int, int],
            end_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> list[tuple[int, int]]:
        stack = deque([start_pos])
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {
                start_pos: None
                }
        visited: set[tuple[int, int]] = set()
        while stack:
            current = stack.popleft()
            if current == end_pos:
                return self._reconstruct_path(start_pos, end_pos, came_from)
            if current in visited:
                continue
            visited.add(current)
            neighboors: list[tuple[int, int]] = self._find_neighboors(
                    maze, current)
            filtered_cells: list[tuple[int, int]] = []
            for cell in neighboors:
                if cell in visited:
                    continue
                filtered_cells.append(cell)
                came_from[cell] = current
            stack.extend(filtered_cells)
        return []

    def _reconstruct_path(
            self,
            start_pos: tuple[int, int],
            end_pos: tuple[int, int],
            came_from: dict[tuple[int, int], tuple[int, int] | None]
    ) -> list[tuple[int, int]]:
        current: tuple[int, int] | None = came_from[end_pos]
        paths: list[tuple[int, int]] = []
        while current is not None:
            if current == start_pos:
                break
            paths.append(current)
            current = came_from[current]
        paths.reverse()
        return paths

    def _find_neighboors(
            self,
            maze: list[list[int]],
            current_cell: tuple[int, int],
    ) -> list[tuple[int, int]]:
        neighboors: list[tuple[int, int]] = []
        x, y = current_cell
        if x - 1 >= 0 and maze[x - 1][y] != 15 and maze[x - 1][y] & EAST == 0:
            neighboors.append((x - 1, y))
        if x + 1 < len(maze) and maze[x + 1][y] != 15 and maze[x + 1][y] & WEST == 0:
            neighboors.append((x + 1, y))
        if y - 1 >= 0 and maze[x][y - 1] != 15 and maze[x][y - 1] & NORTH == 0:
            neighboors.append((x, y - 1))
        if y + 1 < len(maze[0]) and maze[x][y + 1] != 15 and maze[x][y + 1] & SOUTH == 0:
            neighboors.append((x, y + 1))
        return neighboors

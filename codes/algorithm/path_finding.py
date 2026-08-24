from collections import deque

from ..setting import EAST, NORTH, SOUTH, WEST


class Algorithme:
    def __init__(
            self,
            start_pos: tuple[int, int],
            end_pos: tuple[int, int]
    ) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos

    def bfs(self, maze: list[list[int]]) -> list[tuple[int, int]]:
        stack = deque([self.start_pos])
        came_from: dict[
                tuple[int, int], tuple[int, int] | None
                ] = {
                        self.start_pos: None
                }
        seen: set[tuple[int, int]] = set()
        while stack:
            current: tuple[int, int] = stack.popleft()
            if current == self.end_pos:
                return self._reconstruct_path(came_from)
            if current in seen:
                continue
            seen.add(current)
            neighboors = self._find_neighboors(maze, current)
            filtered_neighboors: list[tuple[int, int]] = []
            for cell in neighboors:
                if cell in seen:
                    continue
                came_from[cell] = current
                filtered_neighboors.append(cell)
            print(filtered_neighboors)
            stack.extend(filtered_neighboors)
        return []

    def _reconstruct_path(
            self,
            came_from: dict[tuple[int, int], tuple[int, int] | None]
    ) -> list[tuple[int, int]]:
        current: tuple[int, int] | None = came_from[self.end_pos]
        paths: list[tuple[int, int]] = []
        while current is not None:
            if current == self.start_pos:
                break
            paths.append(current)
            current = came_from[current]
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
            neighboors.append((x - 1, y))
        if y - 1 >= 0 and maze[x][y - 1] != 15 and maze[x][y - 1] & NORTH == 0:
            neighboors.append((x - 1, y))
        if y + 1 < len(maze[0]) and maze[x][y + 1] != 15 and maze[x][y + 1] & SOUTH == 0:
            neighboors.append((x - 1, y))
        return neighboors

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
        while stack:
            ...
        return []

    def _reconstruct_path(
            self,
            came_from: dict[tuple[int, int], tuple[int, int]]
    ) -> list[list[tuple[int, int]]]:
        current: tuple[int, int] = came_from[self.end_pos]
        path: list[tuple[int, int]] = []
        while True:
            if current == self.start_pos:
                break
            path.append(current)
            current = came_from[current]
        return []

    def _find_neighboors(
            self,
            maze: list[tuple[int, int]],
            current_cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        neighboors: list[tuple[int, int]] = []
        _ = NORTH, SOUTH, EAST, WEST
        return neighboors

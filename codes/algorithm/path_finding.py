"""This module contains the path finding Algorithm."""

from typing import Any

from mazegenerator import MazeGenerator

from codes.setting import DIRECTION


class Algorithm:
    """Algorithm class container."""

    def bfs(
        self,
        start_pos: tuple[int, int],
        end_pos: tuple[int, int],
        maze_gen: MazeGenerator,
    ) -> list[tuple[int, int]]:
        """Maze solver algorithm.

        For the algorithm part, we use the one
        provided by the `MazeGenerator` itself
        as we can use this package however we like
        as long as we don't modify it's content.

        Args:
            start_pos: where to start our solver.
            end_pos: where the exit is.
            maze_gen: a MazeGenerator instance.
        Returns:
            paths: a list of cell that leat to `end_pos`
        """
        maze_gen._entryx = start_pos[0]
        maze_gen._entryy = start_pos[1]
        maze_gen._exitx = end_pos[0]
        maze_gen._exity = end_pos[1]
        maze_gen._find_short_path()
        found_path: str | Any = maze_gen.shortest_path
        if not found_path:
            return []
        return self._reconstruct_path(found_path, start_pos)

    def _reconstruct_path(
        self, found_path: str | Any, start_pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        paths: list[tuple[int, int]] = []
        current: tuple[int, int] = start_pos
        for direcition in found_path:
            x: int = current[0] + DIRECTION[direcition][0]
            y: int = current[1] + DIRECTION[direcition][1]
            paths.append((x, y))
            current = paths[-1]
        return paths

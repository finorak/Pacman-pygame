import math
import random
import sys

from codes.setting import EAST, NORTH, SOUTH, WEST


def cell_is_valid(
        current_pos: tuple[int, int],
        new_pos: tuple[int, int],
        maze: list[list[int]]
) -> bool:
    old_x, old_y = current_pos
    new_x, new_y = new_pos
    if (0 > old_x or old_x >= len(maze)) or (0 > old_y or old_y >= len(maze[0])):
        return False
    if (0 > new_x or new_x >= len(maze)) or (0 > new_y or new_y >= len(maze[0])):
        return False
    try:
        if maze[new_x][new_y] == 15:
            return False
        return maze[old_x][old_y] & maze[new_x][new_y] != 0
    except IndexError:
        return False

def get_state(
        target_pos: tuple[int, int],
        current_pos: tuple[int, int]
) -> tuple[int, int]:
    """
    ```
    cur_pos -> target_pos
    (5, 6)  -> (5, 6)
            -> (5, 7)
            -> (4, 6)
            -> (3, 6)
    ```
    """
    cx, cy = current_pos
    tx, ty = target_pos
    if tx == cx:
        if ty > cy:
            return (0, 1)
        return (0, -1)
    if tx > cx:
        return (1, 0)
    return (-1, 0)


def find_cell_neighboors(
    maze: list[list[int]],
    current_cell: tuple[int, int],
) -> list[tuple[int, int]]:
    neighboors: list[tuple[int, int]] = []
    x, y = current_cell
    if x - 1 >= 0 and maze[x - 1][y] != 15 and maze[x - 1][y] & WEST == 0:
        neighboors.append((x - 1, y))
    if x + 1 < len(maze) and maze[x + 1][y] != 15 and maze[x + 1][y] & EAST == 0:
        neighboors.append((x + 1, y))
    if y - 1 >= 0 and maze[x][y - 1] != 15 and maze[x][y - 1] & NORTH == 0:
        neighboors.append((x, y - 1))
    if y + 1 < len(maze[0]) and maze[x][y + 1] != 15 and maze[x][y + 1] & SOUTH == 0:
        neighboors.append((x, y + 1))
    return neighboors

def player_in_range(
        current_pos: tuple[int, int],
        player_pos: tuple[int, int],
        radius: int
) -> bool:
    cx, cy = current_pos
    px, py = player_pos
    x = math.pow(px - cx, 2)
    y = math.pow(py - cy, 2)
    r = math.pow(radius, 2)
    return (x + y) <= r


def test(lst: list[tuple[int, int]]) -> tuple[int, int]:
    ...

def get_valid_gums_coord(
        maze: list[list[int]],
        count: int,
) -> list[tuple[int, int]]:
    paths = [
            (i, j) for i in range(len(maze))
            for j in range(len(maze[0])) if maze[i][j] != 15
            ]
    random.shuffle(paths)
    def get_valid(
        seen: set[tuple[int, int]],
        gum_count: int
    ) -> list[tuple[int, int]]:
        nonlocal paths
        if gum_count == 0:
            return list(seen)
        coord = random.choice(paths)
        if coord in seen or maze[coord[0]][coord[1]] == 15:
            paths.remove(coord)
            seen.remove(coord)
            return get_valid(seen, gum_count)
        seen.add(coord)
        paths.remove(coord)
        return get_valid(seen, gum_count - 1)
    return get_valid(set(), count)

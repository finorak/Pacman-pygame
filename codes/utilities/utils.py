import math
import random

from codes.setting import EAST, NORTH, SOUTH, WEST


def in_bound(x: int, y: int, maze: list[list[int]]) -> bool:
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])

def valid_neighboor(value: int, wall: int) -> bool:
    return value != 15 and value & wall == 0

def cell_is_valid(
        current_pos: tuple[int, int],
        new_pos: tuple[int, int],
        maze: list[list[int]]
) -> bool:
    old_x, old_y = current_pos
    new_x, new_y = new_pos
    if not in_bound(old_x, old_y, maze):
        return False
    if not in_bound(new_x, new_y, maze):
        return False
    if maze[new_x][new_y] == 15:
        return False
    return maze[old_x][old_y] & maze[new_x][new_y] != 0

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
    if in_bound(x - 1, y, maze) and valid_neighboor(maze[x - 1][y], WEST):
        neighboors.append((x - 1, y))
    if in_bound(x + 1, y, maze) and valid_neighboor(maze[x + 1][y], EAST):
        neighboors.append((x + 1, y))
    if in_bound(x, y - 1, maze) and valid_neighboor(maze[x][y - 1], NORTH):
        neighboors.append((x, y - 1))
    if in_bound(x, y + 1, maze) and valid_neighboor(maze[x][y + 1], SOUTH):
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


def wall_closed(value: int, maze: list[list[int]]) -> bool:
    return not (
            valid_neighboor(value, EAST) and valid_neighboor(value, WEST)
            and valid_neighboor(value, NORTH) and valid_neighboor(value, SOUTH)
            )

def get_valid_gums_coord(
        maze: list[list[int]],
        count: int,
) -> list[tuple[int, int]]:
    paths = [
            (i, j) for i in range(len(maze))
            for j in range(len(maze[0]))
            if wall_closed(maze[i][j], maze)
            ]
    random.shuffle(paths)
    valid_coord: list[tuple[int, int]] = []
    for path in paths[:]:
        if count <= 0:
            break
        paths.remove(path)
        valid_coord.append(path)
        count -= 1
    return valid_coord

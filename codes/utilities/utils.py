import json
import math
import sys

from codes.parsing.parse import GameModel
from codes.setting import DIR_BIT, TARGET_DIRECTION


def in_bounds(x: int, y: int, maze: list[list[int]]) -> bool:
    return 0 <= x < len(maze) and 0 <= y < len(maze[0])


def valid_neighboor(value: int, wall: int) -> bool:
    return value != 15 and (value & wall) != 0


def get_direction(
    target_pos: tuple[int, int],
    current_pos: tuple[int, int],
) -> str:
    """
    ```
    cur_pos -> target_pos
    (5, 6)  -> (5, 6)
            -> (5, 7)
            -> (4, 6)
            -> (3, 6)
    ```
    """
    dx: int = target_pos[0] - current_pos[0]
    dy: int = target_pos[1] - current_pos[1]
    return TARGET_DIRECTION[(dx, dy)]


def cell_is_valid(
    current_pos: tuple[int, int],
    new_pos: tuple[int, int],
    maze: list[list[int]],
) -> bool:
    old_x, old_y = current_pos
    new_x, new_y = new_pos
    if not in_bounds(old_x, old_y, maze) or not in_bounds(new_x, new_y, maze):
        return False
    if maze[new_x][new_y] == 15:
        return False
    direction = get_direction(new_pos, current_pos)
    out_bit = DIR_BIT[direction]
    return (maze[old_x][old_y] & out_bit) != 0


def player_in_range(
    current_pos: tuple[float, float],
    player_pos: tuple[float, float],
    radius: float,
) -> bool:
    cx, cy = current_pos
    px, py = player_pos
    x = math.pow(px - cx, 2)
    y = math.pow(py - cy, 2)
    return (x + y) <= math.pow(radius, 2)


def load_data(config_file: str) -> GameModel:
    lines: list[str] = []
    try:
        with open(config_file, mode="r", encoding="utf-8") as f:
            raw_data = f.readlines()
        for line in raw_data:
            curr_line = line.strip()
            if not curr_line or curr_line.startswith("#"):
                continue
            lines.append(curr_line)
        data = json.loads("".join(lines))
        return GameModel.model_validate(data)
    except OSError as e:
        print(
            f"[WARNING] Cannot load file {config_file}: {e}", file=sys.stderr
        )
        print("[WARNING] Default value will be used")
    except ValueError as e:
        print(
            f"[WARNING] Cannot load the file as a json: {e}", file=sys.stderr
        )
        print("[WARNING] Default value will be used")
    return GameModel()

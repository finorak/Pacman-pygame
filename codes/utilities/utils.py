"""Module for functions utilities.

This module helpers for the basic of our implementation.
"""

import json
import math
import sys
from typing import TYPE_CHECKING

from pydantic import ValidationError

from codes.parsing.parse import GameModel
from codes.setting import DIR_BIT, DIR_VEC, TARGET_DIRECTION


def in_bounds(x: int, y: int, maze: list[list[int]]) -> bool:
    """Check wether the coordinate is in bounds.

    Args:
        maze: ad
        x: x coordinate of the cell
        y: y coordinate of the cell
    Returns:
        bound: boolean value that determine if its' in bound.
    """
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze)


def get_center(
    screen_size: tuple[int, int], lengh: float, horizontal: bool = True
) -> int:
    """Extract the center of the screen.

    Args:
        screen_size: the size of the screen.
        lengh: the lengh of the surface.
        horizontal: determine if we want the center \
based on the y coordinate.
    Returns:
        center: the center of the screen an integer.
    """
    if horizontal:
        return int((screen_size[0] - lengh) // 2)
    return int((screen_size[1] - lengh) // 2)


def get_direction(
    target_pos: tuple[int, int],
    current_pos: tuple[int, int],
) -> str:
    """Extract directon based on vector.

    Args:
        target_pos: where the player/ghost goes.
        current_pos: the current_pos of the ghst..
    Returns:
        direction: the direction taken based on the vector.
    ```
    cur_pos -> possible target_pos
    (5, 6)  -> (5, 6)
            -> (5, 7)
            -> (4, 6)
            -> (3, 6)
    ```
    """
    dx: int = target_pos[0] - current_pos[0]
    dy: int = target_pos[1] - current_pos[1]
    return TARGET_DIRECTION[(dx, dy)]


def player_in_range(
    current_pos: tuple[float, float],
    player_pos: tuple[float, float],
    radius: float,
) -> bool:
    """Check for collision.

    Given the current position of player/ghost
    we use this mathematical formula to determin
    if they collid or not based on the provided radius.

    Args:
        current_pos: the current pos of the ghost.
        player_pos: the current pos of the player.
        radius: the radius choosen to determin the range.
    Returns:
        in_range: wether the player is in range or not.
    """
    cx, cy = current_pos
    px, py = player_pos
    x = math.pow(px - cx, 2)
    y = math.pow(py - cy, 2)
    return (x + y) <= math.pow(radius, 2)


def can_move(
    grid_x: int,
    grid_y: int,
    direction: str,
    maze: list[list[int]],
    cheat_mode: bool = False,
) -> bool:
    """Check validity of choosed direction.

    Args:
        grid_x: the x coordinate of the cell.
        grid_y: the y coordinate of the cell.
        direction: the direction choosen one of `up`, `down` \
`right` and `left`
        cheat_mode: this tell us if the player is in cheat mode or not.
    Returns:
        valid: wether the direction is valid or not.
    """
    dx, dy = DIR_VEC[direction]
    nx, ny = grid_x + dx, grid_y + dy

    if not in_bounds(grid_x, grid_y, maze) or not in_bounds(nx, ny, maze):
        return False
    if not TYPE_CHECKING and cheat_mode and maze[ny][nx] != 15:
        return True

    cur_mask = maze[grid_y][grid_x]

    if cur_mask == 15:
        return False

    out_bit = DIR_BIT[direction]

    return (cur_mask & out_bit) == 0


def load_data(config_file: str) -> GameModel:
    """Load game model from a given file.

    Given a file, we try to extract the data inside
    it and if some error where to happen with the config
    we go with the default value of the `GameModel`.

    Args:
        config_file: path to config.
    Returns:
        game_model: the extracted model config.
    """
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
        print("[WARNING] Default value will be used", file=sys.stderr)
    except ValidationError as e:
        for error in e.errors():
            print(
                f"[WARNING] Cannot load the file as json: {error['msg']}",
                file=sys.stderr,
            )
        print("[WARNING] Default value will be used", file=sys.stderr)
    except ValueError as e:
        print(
            f"[WARNING] Cannot load the file as a json: {e}", file=sys.stderr
        )
        print("[WARNING] Default value will be used", file=sys.stderr)
    return GameModel()

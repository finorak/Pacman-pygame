import os
from os import listdir
from typing import Any

import pygame


def get_path(*arg: str) -> str:
    return os.path.join(*arg)


def load_img_from_dir(dir_path: str) -> list[Any]:
    res: list[pygame.Surface] = []
    for file in listdir(dir_path):
        img = pygame.image.load(
                os.path.join(dir_path, file)
            )
        res.append(img)
    return res


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

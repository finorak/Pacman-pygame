import os
from os import listdir
from typing import Any

import pygame


def load_img_dir(dir_path: str) -> list[Any]:
    res: list[pygame.Surface] = []
    for file in listdir(dir_path):
        img = pygame.image.load(
                os.path.join(dir_path, file)
                )
        res.append(img)
    return res

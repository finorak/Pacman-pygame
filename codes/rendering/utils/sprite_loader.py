from os import walk
from os.path import join

import pygame


class SpriteLoader:
    @staticmethod
    def import_image(
        *path: str,
        format: str = "png",
        alpha: bool = True,
    ) -> pygame.Surface:
        full_path = join(*path) + f".{format}"
        return (
            pygame.image.load(full_path).convert_alpha()
            if alpha
            else pygame.image.load(full_path).convert()
        )

    @staticmethod
    def import_folder(*path: str) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        for folder_path, _, file_names in walk(join(*path)):
            for file_name in sorted(
                file_names, key=lambda name: int(name.split(".")[0])
            ):
                full_path = join(folder_path, file_name)
                frames.append(pygame.image.load(full_path).convert_alpha())
        return frames

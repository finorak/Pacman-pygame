"""Module that contains the sprite loader."""

from os import walk
from os.path import join

import pygame


class SpriteLoader:
    """Basic sprite loader that load sprite from file and directory."""

    @staticmethod
    def import_image(
        *path: str,
        format: str = "png",
    ) -> pygame.Surface:
        """
        Import image from a path.

        Args:
            path (str): The path of the file.
            format (str): The format of the file.
        Returns:
            pygame: The surface of the image.
        """
        full_path = join(*path) + f".{format}"
        return pygame.image.load(full_path).convert_alpha()

    @staticmethod
    def import_folder(*path: str) -> list[pygame.Surface]:
        """
        Import every file in a directory as an AnimatedSprite.

        Args:
            path (str): The path of the folder.
        Returns:
            list: the list of surface.
        """
        frames: list[pygame.Surface] = []
        for folder_path, _, file_names in walk(join(*path)):
            for file_name in sorted(
                file_names, key=lambda name: int(name.split(".")[0])
            ):
                full_path = join(folder_path, file_name)
                frames.append(pygame.image.load(full_path).convert_alpha())
        return frames

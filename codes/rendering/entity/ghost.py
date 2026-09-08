import pygame
from pygame.key import ScancodeWrapper
from .entity import Entity
from ..component import AnimatedSprite
from ..utils import SpriteLoader


class Ghost(Entity):
    def __init__(
        self, pos: tuple[int, int], maze: list[list[int]], name: str
    ) -> None:
        self.name = name
        super().__init__(pos, maze)

    def load_image(self) -> dict[str, AnimatedSprite]:
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder(
                    "assets", "ghosts", self.name, direction
                ),
            )
        return result

    def get_input(self, key: ScancodeWrapper) -> None:
        if key[pygame.K_k]:
            self.next_dir = "up"
        if key[pygame.K_j]:
            self.next_dir = "down"
        if key[pygame.K_l]:
            self.next_dir = "right"
        if key[pygame.K_h]:
            self.next_dir = "left"

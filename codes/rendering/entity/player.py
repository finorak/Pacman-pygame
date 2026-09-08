import pygame
from pygame.key import ScancodeWrapper
from .entity import Entity
from ..component import AnimatedSprite
from ..utils import SpriteLoader


class Player(Entity):
    def __init__(self, pos: tuple[int, int], maze: list[list[int]]) -> None:
        super().__init__(pos, maze)

    def load_image(self) -> dict[str, AnimatedSprite]:
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder("assets", "pacman", direction),
            )
        return result

    def get_input(self, key: ScancodeWrapper) -> None:
        if key[pygame.K_w]:
            self.next_dir = "up"
        elif key[pygame.K_s]:
            self.next_dir = "down"
        elif key[pygame.K_d]:
            self.next_dir = "right"
        elif key[pygame.K_a]:
            self.next_dir = "left"

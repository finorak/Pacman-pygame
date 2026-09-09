import pygame
from pygame.key import ScancodeWrapper

from codes.pacgums import Pacgum
from codes.rendering.component import AnimatedSprite
from codes.rendering.utils import SpriteLoader

from .entity import Entity


class Player(Entity):
    def __init__(
            self, pos: tuple[int, int],
            maze: list[list[int]],
            gums: dict[tuple[int, int], Pacgum],
            life: int = 3
    ) -> None:
        super().__init__(pos, maze, life)
        self.can_eat_ghost: bool = False
        self.score: int = 0
        self.gums = gums

    def load_image(self) -> dict[str, AnimatedSprite]:
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder("assets", "pacman", direction),
            )
        return result

    def get_input(self, key: ScancodeWrapper) -> None:
        if self.pos in self.gums and not self.gums[self.pos].eaten: 
            gum = self.gums[self.pos]
            gum.eaten = True
            self.score += gum.score
            print(self.score)
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.next_dir = "up"
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            self.next_dir = "down"
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.next_dir = "right"
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            self.next_dir = "left"

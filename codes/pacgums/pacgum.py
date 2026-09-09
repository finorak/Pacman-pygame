import os

import pygame

from codes.setting import CELL_SIZE


class Pacgum:
    def __init__(
            self,
            pos: tuple[int, int],
            img: str,
            score: int
    ) -> None:
        self.pos = pos
        self.score = score
        self.image = pygame.transform.scale(
                pygame.image.load(
                    os.path.join("assets", "other", img)
                    ), (32, 32)
                )
        self.rect = self.image.get_frect(topleft=pos)
        self.super_gum: bool = False
        self.eaten: bool = False

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(
                self.image,
                (
                    self.pos[0] * CELL_SIZE + 2,
                    self.pos[1] * CELL_SIZE + 2
                )
            )


class SuperGum(Pacgum):
    def __init__(
            self,
            pos: tuple[int, int],
            img: str,
            score: int
    ) -> None:
        super().__init__(pos, img, score)
        self.super_gum = True

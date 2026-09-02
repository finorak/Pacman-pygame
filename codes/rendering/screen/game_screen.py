import pygame

from ..component import Maze, Player
from .base_screen import Screen


class GameScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.maze = Maze((19, 19))
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
        )
        self.player = Player((0,0))

    def get_input(self) -> None: ...

    def update(self, dt: float) -> None:
        self.player.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        self.maze.image.blit(self.player.current_sprite.image)
        self.maze.render(screen)

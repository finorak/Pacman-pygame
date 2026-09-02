import pygame

from ..component import Maze
from .base_screen import Screen


class GameScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.maze = Maze((19, 19))
        self.maze.rect.topleft = self.get_center(self.maze.rect.width), 10

    def get_input(self) -> None: ...

    def update(self, dt: float) -> None: ...

    def render(self, screen: pygame.Surface) -> None:
        self.maze.render(screen)

import pygame

from codes.rendering.component.maze import Maze

from .base_screen import Screen


class GameScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.maze = Maze((19, 19))

    def get_input(self) -> None: ...

    def update(self, dt: float) -> None: ...

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.maze.image)

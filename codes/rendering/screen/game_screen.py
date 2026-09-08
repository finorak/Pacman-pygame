import pygame

from ..component import Maze
from ..entity import Ghost, Player
from .base_screen import Screen


class GameScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.maze = Maze((19, 19))
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
        )
        self.player = Player((0, 0), self.maze.maze)
        self.ghosts = [
            Ghost((18, 18), self.maze.maze, "red"),
            Ghost((0, 0), self.maze.maze, "blue"),
            Ghost((18, 0), self.maze.maze, "yellow"),
            Ghost((0, 18), self.maze.maze, "pink"),
        ]

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
        keys = pygame.key.get_pressed()
        self.player.get_input(keys)
        for ghost in self.ghosts:
            ghost.get_input(keys)

    def update(self, dt: float) -> None:
        self.player.update(dt)
        for ghost in self.ghosts:
            ghost.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        self.player.render(self.maze.image)
        self.maze.render(screen)
        for ghost in self.ghosts:
            ghost.render(self.maze.image)

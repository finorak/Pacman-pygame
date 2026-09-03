import pygame

from .base_screen import Screen


class HighScoreScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

    def update(self, dt: float) -> None: ...

    def render(self, screen: pygame.Surface) -> None: ...

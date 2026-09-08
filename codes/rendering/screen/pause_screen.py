import pygame

from . import Screen


class PauseScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:  # noqa: SIM102
                if event.key == pygame.K_ESCAPE:
                    return "Game"
        return None

    def update(self, dt: float) -> None:
        print(dt)

    def render(self, screen: pygame.Surface) -> None:
        ...

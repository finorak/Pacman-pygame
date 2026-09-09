import pygame

from . import Screen


class PauseScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def enter(self, back: pygame.Surface) -> None:
        self.back = back.copy()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return "Game"
        return None

    def update(self, dt: float) -> None:
        ...

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.back)


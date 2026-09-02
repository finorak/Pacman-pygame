import pygame

from .screen import *


class Rendering:
    def __init__(self, screen_size: tuple[int, int]) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Pac-Man")

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.screens: dict[str, Screen] = {
            "Home": HomeScreen(),
            "HighScore": HighScoreScreen(),
            "Instructions": InstructionsScreen(),
            "Game": GameScreen(),
        }

        self.current_screen = self.screens["Home"]
        self.running = True

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.get_event()
            self.update(dt)
            self.render()

    def get_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.current_screen.get_input()

    def update(self, dt: float) -> None:
        self.current_screen.update(dt)

    def render(self) -> None:
        self.screen.fill((20, 20, 20))
        self.current_screen.render()
        pygame.display.update()

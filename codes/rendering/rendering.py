import pygame

from codes.rendering.utils.sprite_loader import SpriteLoader

from .component import Sprite
from .screen import *


class Rendering:
    def __init__(self, screen_size: tuple[int, int]) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Pac-Man")
        self.screen_size = screen_size

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

        self.load_background()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.get_event()
            self.update(dt)
            self.render()

    def get_event(self) -> None:
        flags = self.current_screen.get_input()
        if flags:
            if flags == "exit":
                self.running = False
                return
            self.current_screen = self.screens[flags]

    def update(self, dt: float) -> None:
        self.background.rect.left -= 30 * dt
        self.current_screen.update(dt)

    def render(self) -> None:
        self._render_background(self.screen)
        self.current_screen.render(self.screen)
        pygame.display.update()

    def load_background(self) -> None:
        self.background = Sprite(
            (0, 0), SpriteLoader.import_image("assets", "background")
        )
        self.background.image = pygame.transform.scale2x(self.background.image)
        self.background.rect = self.background.image.get_frect()

    def _render_background(self, screen: pygame.Surface) -> None:
        image_width = self.background.rect.width

        x = self.background.rect.x

        while x < self.screen_size[0]:
            screen.blit(self.background.image, (x, 0))
            x += image_width

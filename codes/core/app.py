import pygame

from codes.parsing import GameModel
from codes.rendering.component import Sprite
from codes.rendering.screen import (
    GameScreen,
    HighScoreScreen,
    HomeScreen,
    InstructionsScreen,
    PauseScreen,
    Screen,
)
from codes.rendering.utils.sprite_loader import SpriteLoader


class Rendering:
    def __init__(
            self,
            screen_size: tuple[int, int],
            config_file: str
    ) -> None:
        pygame.init()
        self.game_model = GameModel(config_path=config_file)
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
            "pause": PauseScreen()
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
            if isinstance(self.current_screen, PauseScreen):
                self.current_screen.enter(self.screen)

    def update(self, dt: float) -> None:
        if not isinstance(self.current_screen, PauseScreen):
            self.background.rect.left -= 20 * dt
        self.current_screen.update(dt)

    def render(self) -> None:
        if not isinstance(self.current_screen, PauseScreen):
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

"""Module used to combine our implementatoin."""
import pygame

from codes.data.data import Data
from codes.rendering.component import Sprite
from codes.rendering.component.rect import Frect
from codes.rendering.screen import (
    FinishedScreen,
    GameScreen,
    HighScoreScreen,
    HomeScreen,
    InstructionsScreen,
    PauseScreen,
    Screen,
)
from codes.rendering.utils.sprite_loader import SpriteLoader
from codes.setting import BACKGROUND_SPEED, FPS
from codes.utilities import load_data


class Rendering:
    """Class used to combine all our implementatoin of the pac-man \
project."""

    def __init__(self, screen_size: tuple[int, int], config_file: str) -> None:
        """Initialize a `Rendering` class instance.

        Args:
            screen_size: the size of the screen to use.
            config_file: the configuration file provided at runtime.
        """
        pygame.init()
        self.game_model = load_data(config_file)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Pac-Man")
        self.screen_size = screen_size

        self.clock = pygame.time.Clock()
        self.data = Data(self.game_model)

        self.screens: dict[str, Screen] = {
            "Home": HomeScreen(self.game_model, self.data),
            "HighScore": HighScoreScreen(self.game_model, self.data),
            "Instructions": InstructionsScreen(self.game_model, self.data),
            "Game": GameScreen(self.game_model, self.data),
            "pause": PauseScreen(self.game_model, self.data),
            "finished": FinishedScreen(self.game_model, self.data),
        }

        self.current_screen = self.screens["Home"]
        self.running = True

        self.load_background()

    def run(self) -> None:
        """Run the application."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.get_event()
            self.update(dt)
            self.render()

    def get_event(self) -> None:
        """Extract event from the current screen.

        Instead of doing it all in the same function this one \
in this case, we do them in each screen fo better mantainability.
        """
        flags = self.current_screen.get_input()
        if not flags:
            return
        if flags == "new":
            self.data.reset_data(new_game=True)
            flags = "Game"
        if flags == "exit":
            self.running = False
            return
        # This one is a bit redendent, and consume a lot
        # of processing, but it fix bugs so here it is.
        if flags in ("HighScore", "Home", "Instructions"):
            self.data.reset_data(new_game=True)
        self.current_screen = self.screens[flags]
        if isinstance(self.current_screen, PauseScreen):
            self.current_screen.enter(self.screen)
        if flags == "finished" and isinstance(
            self.current_screen, FinishedScreen
        ):
            self.current_screen.enter(self.screen)

    def update(self, dt: float) -> None:
        """Update current screen.

        Args:
            dt: the delta fram used for the frame that occured.
        """
        if not isinstance(self.current_screen, PauseScreen):
            self.background.rect.left -= BACKGROUND_SPEED * dt
        self.current_screen.update(dt)

    def render(self) -> None:
        """Render what happen in the current screen."""
        if not isinstance(self.current_screen, PauseScreen):
            self._render_background(self.screen)
        self.current_screen.render(self.screen)
        pygame.display.update()

    def load_background(self) -> None:
        """Load background onto screen."""
        self.background = Sprite(
            (0, 0), SpriteLoader.import_image("assets", "background")
        )
        self.background.image = pygame.transform.scale2x(self.background.image)
        self.background.rect = Frect(0, 0, self.background.image.width, self.background.image.height)

    def _render_background(self, screen: pygame.Surface) -> None:
        image_width = self.background.rect.width

        x = self.background.rect.x

        while x < self.screen_size[0]:
            screen.blit(self.background.image, (x, 0))
            x += image_width

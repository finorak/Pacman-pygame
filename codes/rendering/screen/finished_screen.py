"""Module that contains the finished screen for the program."""

from os.path import join
from pathlib import Path

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component.button import Button
from codes.rendering.component.sprite import AnimatedSprite
from codes.rendering.screen.base_screen import Screen
from codes.rendering.utils.input import Input
from codes.rendering.utils.sprite_loader import SpriteLoader
from codes.utilities.utils import ressource_path


class FinishedScreen(Screen):
    """The finished screen for the rendering system."""

    def __init__(self, game_model: GameModel, data: Data) -> None:
        """
        Everything starts here.

        Args:
            game_model (GameModel): THe model or variable class for
            the program.
            data (Data): The data that stores every data used during
            the program.
        """
        super().__init__(game_model, data)
        self.background = SpriteLoader.import_image("assets", "hud", "table")
        self.background_rect = (
            self.get_center(self.background.width),
            self.get_center(self.background.height, horizontal=False) - 50,
        )
        self.font = pygame.font.Font(
            Path(
                ressource_path(join("assets", "fonts", "BoldsPixels.ttf"))
                ), 42,
        )
        self.small_font = pygame.font.Font(
            Path(
                ressource_path(join("assets", "fonts", "BoldsPixels.ttf"))
                ), 24,
        )
        self.input = Input(
            (
                self.get_center(400),
                self.background_rect[1] + 125,
            ),
            self.small_font,
            "ENTER YOUR NAME",
        )
        self.buttons: dict[str, Button] = {}
        self.load_buttons()
        self.back = pygame.Surface(self.screen_size)
        self.submitted = False

    @property
    def won(self) -> bool:
        """
        Check if the player won or not.

        Returns:
            bool: true if so.
        """
        return self.data.finished == "win"

    def enter(self, screen: pygame.Surface) -> None:
        """
        Use when we enter the finished screen.

        Args:
            screen (pygame.Surface): The surface to get.
        """
        self.back = screen.copy()
        self.submitted = False
        self.input.active = True

    def get_input(self) -> str | None:
        """
        Get the input from the user.

        Returns:
            str: a signal if there is any.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in self.buttons.values():
                    if button.current_sprite.rect.collidepoint(pos):
                        self.input.text = ''
                        return button.result
            self.input.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self._can_submit():
                    self._save_score()
                    self.input.text = ''
                    return "HighScore"
                elif event.key == pygame.K_ESCAPE:
                    return "Home"
        if not self.input.active:
            return super().get_input()
        return None

    def update(self, dt: float) -> None:
        """
        Update the screen.

        Args:
            dt (float): The delta time.
        """
        self.input.update(dt)
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """
        Render the screen into a surface.

        Args:
            screen (pygame.Surface): The surface to draw the program.
        """
        screen.blit(self.back)
        screen.blit(self.background, self.background_rect)
        title = "YOU WIN!" if self.won else "GAME OVER"
        title_surface = self.font.render(title, True, (255, 255, 0))
        screen.blit(
            title_surface,
            (
                self.get_center(title_surface.get_width()),
                self.background_rect[1] + 35,
            ),
        )
        prompt = self.small_font.render("NAME", True, (255, 255, 255))
        screen.blit(
            prompt,
            (
                self.get_center(prompt.get_width()),
                self.background_rect[1] + 95,
            ),
        )
        self.input.render(screen)
        for button in self.buttons.values():
            button.draw(screen)

    def load_buttons(self) -> None:
        """Load the buttons sprites."""
        buttons = {
            "home": (
                (self.get_center(47) - 120, self.get_center(52, False)),
                "Home",
            ),
            "new": (
                (self.get_center(47) + 120, self.get_center(52, False)),
                "new",
            ),
        }
        for name, (pos, result) in buttons.items():
            sprites = {
                "normal": AnimatedSprite(
                    pos,
                    [
                        self.loader.import_image(
                            "assets", "l_buttons", name, "1"
                        )
                    ],
                ),
                "hover": AnimatedSprite(
                    pos,
                    [
                        self.loader.import_image(
                            "assets", "l_buttons", name, "2"
                        )
                    ],
                ),
                "pressed": AnimatedSprite(
                    pos,
                    self.loader.import_folder("assets", "l_buttons", name),
                ),
            }
            self.buttons[name] = Button(pos, sprites, result)

    def _can_submit(self) -> bool:
        """
        Check if we can submit the input or not.

        Returns:
            bool: True if so.
        """
        name = self.input.text.strip()
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    def _save_score(self) -> None:
        """Save the score in the highscore system."""
        if self.submitted:
            return
        elapsed = max(
            0, int(self.game_model.level_max_time - self.data.player.timer)
        )
        self.data.highscore_loader.add_score(
            self.input.text.strip(), self.data.player.score, elapsed
        )
        self.data.highscore_loader.save(self.data.highscore_loader.highscore)
        self.submitted = True

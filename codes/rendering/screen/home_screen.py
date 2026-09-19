"""Module that contains the home screen for the program."""

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component.sprite import Sprite
from codes.rendering.screen.base_screen import Screen

from ..component import AnimatedSprite, Button


class HomeScreen(Screen):
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
        self.assets: dict[str, AnimatedSprite] = {}
        self.buttons: dict[str, Button] = {}
        self.load_buttons()
        self.load_others()

    def get_input(self) -> str | None:
        """
        Get the input from the user.

        Returns:
            str: a signal if there is any.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result
        return super().get_input()

    def update(self, dt: float) -> None:
        """
        Update the screen.

        Args:
            dt (float): The delta time.
        """
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """
        Render the screen into a surface.

        Args:
            screen (pygame.Surface): The surface to draw the program.
        """
        screen.blit(self.logo.image, self.logo.rect)
        for a in self.assets.values():
            screen.blit(a.image, a.rect)
        for b in self.buttons.values():
            b.draw(screen)

    def load_assets(self) -> dict[str, AnimatedSprite]:
        """
        Load assets from file.

        Returns:
            dict: A dict containing the assets.
        """
        image_path = {"logo": ("assets", "Logo")}
        for name, path in image_path.items():
            self.assets[name] = AnimatedSprite(
                (0, 0), [self.loader.import_image(*path)]
            )
        return self.assets

    def load_buttons(self) -> None:
        """Load the buttons sprites."""
        buttons = {
            "start": ((220, 250), "Game"),
            "instructions": ((220, 310), "Instructions"),
            "highscore": ((220, 370), "HighScore"),
            "exit": ((220, 430), "exit"),
        }
        for button, (pos, result) in buttons.items():
            tmp = {}
            tmp["normal"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "button", button, "1")],
            )
            tmp["hover"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "button", button, "2")],
            )
            tmp["pressed"] = AnimatedSprite(
                pos,
                self.loader.import_folder("assets", "button", button),
            )
            a = Button(pos, tmp, result)
            self.buttons[button] = a

    def load_others(self) -> None:
        """Load other important sprite."""
        self.logo = Sprite(
            (0, 0),
            self.loader.import_image("assets", "Logo"),
        )

        self.logo.position = (
            75,
            30,
        )

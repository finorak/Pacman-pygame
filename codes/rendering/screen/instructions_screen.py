"""Module that contains the instruction screen for the program."""

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component.button import Button
from codes.rendering.screen.base_screen import Screen

from ..component import AnimatedSprite


class InstructionsScreen(Screen):
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
        self.assets = self.load_assets()
        self.buttons: dict[str, Button] = {}
        self.load_buttons()

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Home"
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
        screen.blit(
            self.assets["logo"].image, self.assets["logo"].rect.topleft
        )
        for a in self.buttons.values():
            a.draw(screen)

    def load_assets(self) -> dict[str, AnimatedSprite]:
        """
        Load assets from file.

        Returns:
            dict: A dict containing the assets.
        """
        image_path = {"logo": ("assets", "instructions")}
        result = {}
        for name, path in image_path.items():
            result[name] = AnimatedSprite(
                (0, 0), [self.loader.import_image(*path)]
            )
        return result

    def load_buttons(self) -> None:
        """Load the buttons sprites."""
        buttons = {
            "exit": ((self.screen_size[0] - 60, 5), "Home"),
        }
        for button, (pos, result) in buttons.items():
            tmp = {}
            tmp["normal"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "l_buttons", button, "1")],
            )
            tmp["hover"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "l_buttons", button, "2")],
            )
            tmp["pressed"] = AnimatedSprite(
                pos,
                self.loader.import_folder("assets", "l_buttons", button),
            )
            a = Button(pos, tmp, result)
            self.buttons[button] = a

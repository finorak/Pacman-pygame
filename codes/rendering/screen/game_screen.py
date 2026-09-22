"""Module that contains the game screen for the program."""

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component import (
    AnimatedSprite,
    Button,
)
from codes.rendering.screen.base_screen import Screen
from codes.rendering.ui.ui import UI
from codes.setting import CURRENT_SCREEN_PADDING


class GameScreen(Screen):
    """The game screen for the rendering system."""

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
        self.activate_cheat: bool = False
        self.ui = UI(self.data.player)
        self.buttons: dict[str, Button] = {}

    def get_input(self) -> str | None:
        """Get the input from the user."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_c]:
            self.activate_cheat = not self.activate_cheat
            self.data.player.cheat_mode = self.activate_cheat
        if keys[pygame.K_ESCAPE]:
            return "pause"
        player_output = self.data.player.get_input(keys)
        if player_output:
            return player_output
        if self.data.finished:
            return "finished"
        for ghost in self.data.ghosts:
            ghost.get_input(self.data.player)
        return super().get_input()

    def update(self, dt: float) -> None:
        """
        Update the screen.

        Args:
            dt (float): The delta time.
        """
        self.data._go_to_next_level()
        for ghost in self.data.ghosts:
            ghost.update(dt)
        self.data.player.update(dt)
        for button in self.buttons.values():
            button.update(dt)
        self.ui.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """
        Render the screen into a surface.

        Args:
            screen (pygame.Surface): The surface to draw the program.
        """
        self.data.maze.render(screen)
        self.data.pacgums.render(self.data.maze.image)
        for ghost in self.data.ghosts:
            ghost.render(self.data.maze.image)
        for a in self.buttons.values():
            a.draw(screen)
        self.ui.render(screen)
        self.data.player.render(self.data.maze.image)

    def load_buttons(self) -> None:
        """Load the buttons sprites."""
        buttons = {
            "exit": (
                (
                    self.screen_size[0] - CURRENT_SCREEN_PADDING[0],
                    CURRENT_SCREEN_PADDING[1],
                ),
                "pause",
            ),
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

    def new(self) -> None:
        """Make a new player and ghost and maze."""
        self.data.maze.reset()
        self.data.player.reset()
        for ghost in self.data.ghosts:
            ghost.reset()

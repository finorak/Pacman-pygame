"""Module that contains the UI class."""

from os.path import join
from pathlib import Path

import pygame

from codes.setting import SCREEN_SIZE
from codes.utilities.utils import ressource_path

from ...entity import Player
from ..utils import SpriteLoader

# In-Game HUD (always visible during gameplay):
# ◦ Current score
# ◦ Remaining lives
# ◦ Current level
# ◦ Remaining time for the level


class UI:
    """Basic UI class for the main game loop."""

    def __init__(self, player: Player) -> None:
        """
        Everything starts here.

        Args:
            player (Player): The player as a class.
        """
        self.surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)

        self.player = player
        self.background = SpriteLoader.import_image(
            "assets", "hud", "background"
        )

        self.heart = SpriteLoader.import_image("assets", "hud", "heart")

        self.font = pygame.Font(
            Path(
                ressource_path(join("assets", "fonts", "BoldsPixels.ttf")),
                ), size=23
        )

        self.current_level_surface = self.font.render(
            f"LEVEL: {self.player.level}", True, "white"
        )
        self.current_level = self.player.level

        self.current_score_surface = self.font.render(
            f"SCORE: {self.player.score}", True, "white"
        )
        self.current_score = self.player.score

    def render(self, screen: pygame.Surface) -> None:
        """
        Render the screen into a surface.

        Args:
            screen (pygame.Surface): The surface to draw the program.
        """
        cheat_mode_surface = self.font.render(
            f"CHEAT: {self.player.cheat_mode}", True, "white"
        )
        self.surface.blit(self.background, (10, 50))

        self.draw_heart(self.surface)
        self.draw_time(self.surface)
        self.surface.blit(self.current_level_surface, (60, 198))
        self.surface.blit(self.current_score_surface, (60, 233))
        self.surface.blit(cheat_mode_surface, (60, 350))
        screen.blit(self.surface)

    def update(self, dt: float) -> None:
        """
        Update the screen.

        Args:
            dt (float): The delta time.
        """
        if self.player.level != self.current_level:
            self.current_level_surface = self.font.render(
                f"LEVEL: {self.player.level}", True, "white"
            )
            self.current_level = self.player.level
        if self.player.score != self.current_score:
            self.current_score_surface = self.font.render(
                f"SCORE: {self.player.score}", True, "white"
            )
            self.current_score = self.player.score

    def draw_heart(self, surface: pygame.Surface) -> None:
        """
        Draw a heart to represent a life.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        value = self.player.life
        surface.blit(self.font.render("LIFE: ", True, "white"), (60, 105))
        if value < 5:
            for i in range(value):
                surface.blit(self.heart, (120 + 30 * i, 100))
            return
        for i in range(4):
            surface.blit(self.heart, (120 + 30 * i, 100))
        for i in range(min(value - 4, 6)):
            surface.blit(self.heart, (60 + 30 * i, 132))

    def draw_time(self, surface: pygame.Surface) -> None:
        """
        Draw a time to represent the remaining time.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        player_timer = max(0, self.player.timer)
        surface.blit(
            self.font.render(f"TIME: {player_timer:.0f}", True, "white"),
            (60, 165),
        )

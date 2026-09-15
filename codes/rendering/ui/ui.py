from pathlib import Path

import pygame

from codes.setting import SCREEN_SIZE

from ...players import Player
from ..utils import SpriteLoader

# In-Game HUD (always visible during gameplay):
# ◦ Current score
# ◦ Remaining lives
# ◦ Current level
# ◦ Remaining time for the level


class UI:
    def __init__(self, player: Player) -> None:
        self.surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)

        self.player = player
        self.background = SpriteLoader.import_image(
            "assets", "hud", "background"
        )

        self.heart = SpriteLoader.import_image("assets", "hud", "heart")

        self.font = pygame.Font(
            Path("assets", "fonts", "BoldsPixels.ttf"), size=23
        )

        self.current_level_surface = self.font.render(f"LEVEL: {self.player.level}", True, "white")
        self.current_level = self.player.level

        self.current_score_surface = self.font.render(f"SCORE: {self.player.level}", True, "white")
        self.current_score = self.player.score

    def render(self, screen: pygame.Surface) -> None:
        self.surface.blit(self.background, (10, 50))
        self.draw_heart(self.surface)
        self.draw_time(self.surface)
        self.surface.blit(self.current_level_surface, (60, 198))
        self.surface.blit(self.current_score_surface, (60, 233))
        screen.blit(self.surface)

    def update(self, dt: float) -> None:
        if self.player.level != self.current_level:
            self.current_level_surface = self.font.render(f"LEVEL: {self.player.level}", True, "white")
            self.current_level = self.player.level
        if self.player.score != self.current_score:
            self.current_score_surface = self.font.render(f"SCORE: {self.player.score}", True, "white")
            self.current_score = self.player.score

    def draw_heart(self, surface: pygame.Surface) -> None:
        value = self.player.life
        surface.blit(self.font.render("LIFE: ", True, "white"), (60, 105))
        if value < 5:
            for i in range(value):
                surface.blit(self.heart, (120 + 30 * i, 100))
        else:
            for i in range(4):
                surface.blit(self.heart, (120 + 30 * i, 100))
            for i in range(min(value - 4, 6)):
                surface.blit(self.heart, (60 + 30 * i, 132))

    def draw_time(self, surface: pygame.Surface) -> None:
        surface.blit(
            self.font.render(f"TIME: {self.player.timer:.0f}", True, "white"),
            (60, 165),
        )

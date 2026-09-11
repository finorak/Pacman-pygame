import pygame

from codes.rendering.utils.sprite_loader import SpriteLoader

from ...setting import SCREEN_SIZE

"""This module contains the basic UI info and logic for the game part of the project."""


# In-Game HUD (always visible during gameplay):
# ◦ Current score
# ◦ Remaining lives
# ◦ Current level
# ◦ Remaining time for the level
class HUD:
    def __init__(self) -> None:
        self.load_assets()
        self.font = pygame.Font("assets/fonts/BoldsPixels.ttf", size=32)

        self.score: int = 0
        self.remaining_time: float = 0.0
        self.current_level = 0
        self.lives = 0

        self.surface = pygame.Surface(
            SCREEN_SIZE, pygame.SRCALPHA, 32
        ).convert_alpha()
        self.running = True

    def render(self, screen: pygame.Surface) -> None:
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.background, (25, 25))
        hp_text = self.font.render(f"Lives: {self.lives:02}", True, "WHITE")
        self.surface.blit(hp_text, (80, 75))
        current_score = self.font.render(f"Score: {self.score:02}", True, "WHITE")
        self.surface.blit(current_score, (80, 115))
        current_level = self.font.render(
            f"Level: {self.current_level:02}", True, "WHITE"
        )
        self.surface.blit(current_level, (80, 155))
        remaining_time = self.font.render(
            f"Time Remaining:\n{self.remaining_time:02.1f}", True, "WHITE"
        )
        self.surface.blit(remaining_time, (80, 195))
        screen.blit(self.surface)

    def update(self, dt: float) -> None:
        if not self.running:
            return
        self.remaining_time += dt

    def add_score(self, value: int) -> None:
        self.score += value

    def set_values(
        self,
        remaining_time: float,
        lives: int,
        current_level: int,
        score: int = 0,
    ) -> None:
        self.score = score
        self.remaining_time = remaining_time
        self.lives = lives
        self.current_level = current_level

    def load_assets(self) -> None:
        self.background = SpriteLoader.import_image(
            "assets", "hud", "background"
        )

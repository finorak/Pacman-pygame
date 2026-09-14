from pathlib import Path

import pygame

from codes.setting import SCREEN_SIZE

from ..utils import SpriteLoader

# In-Game HUD (always visible during gameplay):
# ◦ Current score
# ◦ Remaining lives
# ◦ Current level
# ◦ Remaining time for the level


class UI:
    def __init__(self) -> None:
        self.surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)

        self.background = SpriteLoader.import_image("assets", "hud", "background")
        self.heart = SpriteLoader.import_image("assets", "hud", "heart")
        self.lives_remaining = 3
        self.current_score = 0
        self.current_level = 0
        self.remaining_time = 0

        self.font = pygame.Font(Path("assets", "fonts", "BoldsPixels.ttf"), size=23)
        self.draw_heart(self.background)

    def update(self, dt: float) -> None: ...

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (10, 50))

    def draw_heart(self, surface: pygame.Surface) -> None:
        for i in range(self.lives_remaining):
            surface.blit(self.font.render("LIFE: ", True, "white"), (50, 60))
            surface.blit(self.heart, (120 + 30 * i, 50))

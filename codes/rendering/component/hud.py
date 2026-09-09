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
        self.font = pygame.Font()
        self.score: int = 0
        self.remaining_time: float = 0.0
        self.current_level = 0
        self.lives = 0

        self.surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32).convert_alpha()
        self.running = False

    def render(self, screen: pygame.Surface) -> None:
        self.surface.blit(self.background, (25, 25))
        screen.blit(self.surface)

    def update(self, dt: float) -> None:
        if not self.running:
            return
        self.remaining_time += dt

    def update_surface(self) -> None: ...

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

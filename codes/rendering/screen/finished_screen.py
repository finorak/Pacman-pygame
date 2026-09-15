from os.path import join

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.screen.base_screen import Screen
from codes.rendering.utils.input import Input
from codes.rendering.utils.sprite_loader import SpriteLoader


class FinishedScreen(Screen):
    def __init__(self, game_model: GameModel, data: Data) -> None:
        super().__init__(game_model, data)
        self.fonts = pygame.font.Font(join("assets", "fonts", "BoldsPixels.ttf"), 48)
        self.background = SpriteLoader.import_image(
            "assets", "hud", "background"
        )
        self.input = Input(
            (100, 100),
            self.fonts,
        )
        self.timer = 0.0

    def render(self, screen: pygame.Surface) -> None:
        self.input.render(screen)

    def update(self, dt: float) -> None:
        self.timer += dt
        self.input.update(dt)

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            self.input.handle_event(event)
            if event.type == pygame.QUIT:
                return "exit"

    def get_player_highscore(self) -> None: ...

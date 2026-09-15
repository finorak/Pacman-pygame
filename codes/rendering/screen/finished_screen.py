import pygame

from codes.parsing.parse import GameModel
from codes.rendering.screen.data import Data
from codes.rendering.utils.sprite_loader import SpriteLoader


class FinishedScreen(Data):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(game_model)
        self.background = SpriteLoader.import_image(
            "assets", "hud", "background"
        )

    def render(self, screen: pygame.Surface) -> None: ...

    def update(self, dt: float) -> None: ...

    def get_input(self) -> str | None: ...

from pathlib import Path

import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component.button import Button
from codes.rendering.screen.base_screen import Screen

from ...highscore import HighScoreLoader
from ..component import AnimatedSprite


class HighScoreScreen(Screen):
    def __init__(self, game_model: GameModel, data: Data) -> None:
        super().__init__(game_model, data)

        self.logo = self.load_logo()
        self.buttons: dict[str, Button] = {}
        self.load_buttons()
        self.highscore_loader = HighScoreLoader(Path("data", "highscore.json"))

        self.fonts = pygame.Font(
            Path("assets", "fonts", "BoldsPixels.ttf"), size=32
        )
        self.leaderboard = self.draw_leaderboard()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result
        return None

    def update(self, dt: float) -> None:
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.logo.image, self.logo.rect)
        for a in self.buttons.values():
            a.draw(screen)
        screen.blit(self.leaderboard)

    def load_logo(self) -> AnimatedSprite:
        path = ("assets", "highscore", "Logo")
        return AnimatedSprite((470, 50), [self.loader.import_image(*path)])

    def draw_leaderboard(self) -> pygame.Surface:
        surface = pygame.Surface(
            self.screen_size, pygame.SRCALPHA, 32
        ).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for i, score in enumerate(self.highscore_loader.highscore, 1):
            if i == 1:
                text = self.fonts.render(
                    f"{i:02} - {score.player_name}: {score.player_score}",
                    True,
                    "red",
                )
            elif i == 2:
                text = self.fonts.render(
                    f"{i:02} - {score.player_name}: {score.player_score}",
                    True,
                    "gold",
                )
            elif i == 3:
                text = self.fonts.render(
                    f"{i:02} - {score.player_name}: {score.player_score}",
                    True,
                    "pink",
                )
            else:
                text = self.fonts.render(
                    f"{i:02} - {score.player_name}: {score.player_score}",
                    True,
                    (230, 230, 230),
                )
            surface.blit(
                text,
                (self.get_center(text.width), i * 50 + 100),
            )
        return surface

    def load_buttons(self) -> None:
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

import random
from pathlib import Path

from codes.parsing.parse import GameModel
from codes.rendering.component.button import Button

from ..component import AnimatedSprite
from .data import Data
import pygame

from ...highscore import HighScoreLoader, HighScoreModel
from ..component import AnimatedSprite, Button
from .base_screen import Screen


class HighScoreScreen(Data):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(game_model)

        self.logo = self.load_logo()
        self.buttons = {}
        self.load_buttons()
        self.highscore_loader = HighScoreLoader(Path("data", "highscore.json"))
        self.highscore: list[HighScoreModel] = self.highscore_loader.highscore

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
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_1]:
            self.highscore_loader.add_score("aaaa", random.randint(100, 100000))
            self.leaderboard = self.draw_leaderboard()
            self.highscore = self.highscore_loader.highscore

    def update(self, dt: float) -> None:
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.logo.image, self.logo.rect)
        for a in self.buttons.values():
            a.draw(screen)
        screen.blit(self.leaderboard, (100, 100))

    def load_logo(self) -> AnimatedSprite:
        path = ("assets", "highscore", "Logo")
        return AnimatedSprite((100, 40), [self.loader.import_image(*path)])

    def draw_leaderboard(self) -> pygame.Surface:
        surface = pygame.Surface(self.screen_size).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for i, score in enumerate(self.highscore, 1):
            text = self.fonts.render(
                f"{i:02} - {score.player_name}: {score.player_score}",
                True,
                "yellow",
            )
            surface.blit(text, (0, i * 50))
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

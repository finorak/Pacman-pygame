import pygame

from codes.parsing.parse import GameModel
from codes.rendering.component import (
    AnimatedSprite,
    Button,
)
from codes.setting import CURRENT_SCREEN_PADDING

from .data import Data


class GameScreen(Data):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(game_model)

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return "pause"
        self.player.get_input(keys)
        for ghost in self.ghosts:
            ghost.get_input(self.player)

    def update(self, dt: float) -> None:
        self.player.update(dt)
        for ghost in self.ghosts:
            ghost.update(dt)
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        self.maze.render(screen)
        self.pacgums.render(self.maze.image)
        self.player.render(self.maze.image)
        for ghost in self.ghosts:
            ghost.render(self.maze.image)
        for a in self.buttons.values():
            a.draw(screen)

    def load_buttons(self) -> None:
        buttons = {
            "exit": ((self.screen_size[0] - CURRENT_SCREEN_PADDING[0], CURRENT_SCREEN_PADDING[1]), "pause"),
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

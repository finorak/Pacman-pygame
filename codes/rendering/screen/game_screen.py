import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component import (
    AnimatedSprite,
    Button,
)
from codes.rendering.screen.base_screen import Screen
from codes.rendering.ui.ui import UI
from codes.setting import CURRENT_SCREEN_PADDING


class GameScreen(Screen):
    def __init__(self, game_model: GameModel, data: Data) -> None:
        super().__init__(game_model, data)
        self.activate_cheat: bool = False
        self.ui = UI(self.data.player)
        self.buttons: dict[str, Button] = {}

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
        if keys[pygame.K_c]:
            self.activate_cheat = not self.activate_cheat
            self.data.player.cheat_mode = self.activate_cheat
        if keys[pygame.K_ESCAPE]:
            return "pause"
        player_output = self.data.player.get_input(keys)
        if player_output:
            return player_output
        for ghost in self.data.ghosts:
            ghost.get_input(self.data.player)
        return None

    def update(self, dt: float) -> None:
        self.data._go_to_next_level()
        self.data.player.update(dt)
        for ghost in self.data.ghosts:
            ghost.update(dt)
        for button in self.buttons.values():
            button.update(dt)
        self.ui.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        self.data.maze.render(screen)
        self.ui.render(screen)
        self.data.pacgums.render(self.data.maze.image)
        self.data.player.render(self.data.maze.image)
        for ghost in self.data.ghosts:
            ghost.render(self.data.maze.image)
            for a in self.buttons.values():
                a.draw(screen)

    def load_buttons(self) -> None:
        buttons = {
            "exit": (
                (
                    self.screen_size[0] - CURRENT_SCREEN_PADDING[0],
                    CURRENT_SCREEN_PADDING[1],
                ),
                "pause",
            ),
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

    def new(self) -> None:
        self.data.maze.reset()
        self.data.player._reset()
        for ghost in self.data.ghosts:
            ghost._reset()

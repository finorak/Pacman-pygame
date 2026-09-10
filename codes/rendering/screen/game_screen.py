from typing import Any

import pygame

from codes.pacgums import Pacgum
from codes.pacgums.pacgum import SuperGum
from codes.parsing.parse import GameModel
from codes.players import Ghost, Player
from codes.rendering.component import (
    AnimatedSprite,
    Button,
    Maze,
)
from codes.utilities import get_valid_gums_coord

from .base_screen import Screen


class GameScreen(Screen):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(game_model)
        self.maze = Maze((19, 19), self.game_model.seed)
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
        )
        self.valid_gum_places = get_valid_gums_coord(
                self.maze.maze,
                self.game_model.pacgum_number + self.game_model.super_pacgum_number
                )
        self.gume_dict: dict[tuple[int, int], Pacgum] = {
                gum.pos: gum for gum in [
                    Pacgum(
                        (i, j), "strawberry.png",
                        self.game_model.points_per_pacgum
                        )
                    for (i, j) in self.valid_gum_places
                    if (i, j) not in [(0, 0), (0, 18), (18, 0), (18, 18)]
                    ]
                }
        for coord in [(0, 0), (0, 18), (18, 0), (18, 18)]:
            self.gume_dict[coord] =  SuperGum(
                            coord, "apple.png",
                            self.game_model.points_per_super_pacgum
                            )
        self.player = Player(
                (9, 9), self.maze.maze, self.gume_dict,
                self.game_model.player_life
            )
        self.ghosts = [
            Ghost((18, 18), self.maze.maze, "red", self.game_model.points_per_ghost),
            Ghost((0, 0), self.maze.maze, "blue", self.game_model.points_per_ghost),
            Ghost((18, 0),  self.maze.maze, "yellow", self.game_model.points_per_ghost),
            Ghost((0, 18),  self.maze.maze, "pink", self.game_model.points_per_ghost),
        ]
        self.buttons: dict[str, Any] = {}

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
        self.player.get_input(keys, Ghost)
        for ghost in self.ghosts:
            ghost.get_input(self.player)

    def update(self, dt: float) -> None:
        self.player.update(dt)
        for ghost in self.ghosts:
            ghost.update(dt)
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        self.player.render(self.maze.image)
        self.maze.render(screen)
        for gum_coord in self.gume_dict:
            gum = self.gume_dict[gum_coord]
            if gum.eaten:
                continue
            gum.render(self.maze.image)
        for ghost in self.ghosts:
            ghost.render(self.maze.image)
        for a in self.buttons.values():
            a.draw(screen)

    def load_buttons(self) -> None:
        buttons = {
            "exit": ((self.screen_size[0] - 60, 5), "pause"),
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

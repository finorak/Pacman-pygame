from typing import Any

import pygame

from codes.players import Ghost, Player
from codes.rendering.component import AnimatedSprite, Button, Maze

from .base_screen import Screen


class GameScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.maze = Maze((19, 19))
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
        )
        self.player = Player((len(self.maze.maze) // 2, len(self.maze.maze[0]) // 2), self.maze.maze)
        self.ghosts = [
            Ghost((18, 18), self.maze.maze, "red"),
            Ghost((0, 0), self.maze.maze, "blue"),
            Ghost((18, 0), self.maze.maze, "yellow"),
            Ghost((0, 18), self.maze.maze, "pink"),
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
        self.player.render(self.maze.image)
        self.maze.render(screen)
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

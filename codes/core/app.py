import os

import pygame
from mazegenerator import MazeGenerator

from codes.algorithm.path_finding import Algorithme
from codes.parsing.parse import GameModel
from codes.players.ghost import Ghost
from codes.players.player import Player
from codes.utilities.utils import get_path, load_img_from_dir


class Data:
    def __init__(self, config_path: str) -> None:
        pygame.init()
        self.data = GameModel(config_path=config_path)
        self.maze_gen = MazeGenerator(
                size=(16, 16),
                seed=self.data.seed
                )
        algorithm = Algorithme()
        paths = algorithm.bfs((0, 0), (15, 15), self.maze_gen.maze)
        for index, cell in enumerate(paths):
            print(cell, end=" => " if index < len(paths) else "\n")
        self.load_asset()

    def load_asset(self, ) -> None:
        # TODO: MIGHT PUT THESE INSIDE `setting` later on.
        self.player_frames: dict[str, list[pygame.Surface]] = {
            player_direction.split("-")[-1]: load_img_from_dir(
                get_path("assets", "pacman", player_direction))
            for player_direction in os.listdir(
                get_path("assets", "pacman")
                )
        }
        self.ghost_frames: dict[str, dict[str, list[pygame.Surface]]] = {
                ghost_color: {
                    ghost_direction.split("-")[-1]: load_img_from_dir(
                        get_path(
                            "assets", "ghosts", ghost_color, ghost_direction
                            )
                        )
                    for ghost_direction in os.listdir(
                        get_path(
                            "assets", "ghosts", ghost_color
                            )
                        )
                    }
                for ghost_color in os.listdir(
                    get_path("assets", "ghosts")
                    )
                }


class App(Data):
    def __init__(
            self,
            config_path: str,
            screen_size: tuple[int, int] = (1280, 950)
    ) -> None:
        super().__init__(config_path)
        self.screen = pygame.display.set_mode(screen_size)
        self.player = Player(
                self.player_frames,
                (0, 0),
                self.data.player_life
                )
        self.ghosts = [
                Ghost(
                    self.ghost_frames[ghost_color],
                    pos=(0, 0),
                    life=1
                    )
                for ghost_color in self.ghost_frames
                ]
        pygame.display.set_caption("Pacman")

    def run(self) -> None:
        running: bool = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            self.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            self.update(dt, self.player.pos, self.maze_gen.maze)

    def draw(self, screen: pygame.Surface) -> None:
        self.screen.fill("black")
        self.player.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)

    def update(
            self, dt: float, player_pos: tuple[int, int],
            maze: list[list[int]]
    ) -> None:
        pygame.display.update()
        self.player.update(dt, maze)
        for ghost in self.ghosts:
            ghost.update(dt, player_pos, maze)

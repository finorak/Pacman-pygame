import os

import pygame

# from codes.players.ghost import Ghost
from mazegenerator import MazeGenerator

from codes.parsing.parse import GameModel
from codes.players.player import Player
from codes.utilities.utils import load_img_dir


class Data:
    def __init__(self, config_path: str) -> None:
        pygame.init()
        self.data = GameModel(config_path=config_path)
        self.maze_gen = MazeGenerator()
        self.load_asset()

    def load_asset(self, ) -> None:
        self.player_frames: dict[str, list[pygame.Surface]] = {
            dir_.split("-")[-1]:load_img_dir(os.path.join("assets", "pacman", dir_))
            for dir_ in os.listdir(os.path.join("assets", "pacman"))
        }


class App(Data):
    def __init__(self, config_path) -> None:
        super().__init__(config_path)
        self.screen = pygame.display.set_mode((1280, 950))
        self.player = Player(self.player_frames, (0, 0), 3)
        pygame.display.set_caption("Pacman")

    def run(self) -> None:
        running: bool = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            self.player.get_input()
            self.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            self.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.screen.fill("white")
        self.player.draw(screen)

    def update(self, dt: float) -> None:
        pygame.display.update()
        self.player.update(dt)

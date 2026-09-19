"""Data module container for a smooth management."""

import gc
from pathlib import Path

from codes.entity.ghost import Ghost
from codes.entity.player import Player
from codes.highscore import HighScoreLoader
from codes.pacgums.pacgums import Pacgums
from codes.parsing.parse import GameModel
from codes.rendering.component.maze import Maze
from codes.setting import GHOST_START_SETTING, SCREEN_SIZE
from codes.utilities import get_center


class Data:
    """Class used to store all necessary data for our project."""

    def __init__(self, game_model: GameModel) -> None:
        """Initialize a `Data` class instance.

        Args:
            game_model: config for the game.
        """
        self.game_model = game_model
        self.finished: str | None = None

        self.screen_size = SCREEN_SIZE

        self.maze = Maze((19, 19), game_model.seed)
        self.maze.rect.topleft = self.maze_render_pos = (
            get_center(self.screen_size, self.maze.rect.width),
            get_center(
                self.screen_size, self.maze.rect.height, horizontal=False
            ),
        )
        self.pacgums = Pacgums(
            self.maze.maze,
            self.game_model.points_per_pacgum,
            self.game_model.points_per_super_pacgum,
        )
        self.pacgums.generate_gums(self.game_model.pacgum_number)
        self.player = Player(
            (9, 9),
            self.maze.maze,
            self.pacgums,
            self.game_model.life,
            self.game_model.level_max_time,
        )
        self.ghosts = [
            Ghost(
                GHOST_START_SETTING[color]["coord"],
                self.maze.maze,
                color,
                self.game_model.points_per_ghost,
                self.maze.maze_gen,
            )
            for color in GHOST_START_SETTING
        ]

        self.highscore_loader = HighScoreLoader(Path("data", "highscore.json"))

    @property
    def switch_level(self) -> bool:
        """This decide wether we should switch a level or not."""
        return self.pacgums.is_empty

    def reset_data(self, new_game: bool = False) -> None:
        """Reset the data after a game over of new game.

        Args:
            new_game: weather to to a start from scratch or not.
        """
        self.finished = None
        # delete from memory
        del self.maze
        gc.collect()
        if new_game:
            self.maze = Maze((19, 19), seed=self.game_model.seed)
        else:
            self.maze = Maze((19, 19))
        self.maze.rect.topleft = self.maze_render_pos
        self.pacgums.generate_gums(self.game_model.pacgum_number)
        self.player.maze = self.maze.maze
        if new_game:
            self.player.new_game()
        else:
            self.player.reset()
        for ghost in self.ghosts:
            ghost.maze = self.maze.maze
            ghost.maze_gen = self.maze.maze_gen
            ghost.reset()

    def _go_to_next_level(self) -> None:
        if not self.switch_level:
            return
        if self.player.level >= self.game_model.level_count:
            self.finished = "win"
            return
        self.player.timer = self.game_model.level_max_time
        self.player.level += 1
        self.reset_data()

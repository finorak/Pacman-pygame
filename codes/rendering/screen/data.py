import gc

from codes.pacgums.pacgums import Pacgums
from codes.parsing.parse import GameModel
from codes.players import Ghost, Player
from codes.rendering.component.button import Button
from codes.rendering.component.maze import Maze
from codes.rendering.screen.base_screen import Screen
from codes.setting import GHOST_START_SETTING


class Data(Screen):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(game_model)
        self.maze = Maze((19, 19), game_model.seed)
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
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
        self.buttons: dict[str, Button] = {}

    @property
    def switch_level(self) -> bool:
        return self.pacgums.is_empty

    def reset_data(self) -> None:
        # delete from memory
        del self.maze
        gc.collect()
        self.maze = Maze((19, 19))
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
        )
        self.pacgums.generate_gums(self.game_model.pacgum_number)
        self.player.maze = self.maze.maze
        self.player._reset()
        for ghost in self.ghosts:
            ghost.maze = self.maze.maze
            ghost.maze_gen = self.maze.maze_gen
            ghost._reset()

    def _go_to_next_level(self) -> None:
        if not self.switch_level:
            return
        self.player.timer = self.game_model.level_max_time
        self.player.level += 1
        self.reset_data()

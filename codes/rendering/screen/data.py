from typing import Any

from codes.pacgums.pacgums import Pacgums
from codes.parsing.parse import GameModel
from codes.players import Ghost, Player
from codes.rendering.component.maze import Maze
from codes.rendering.screen.base_screen import Screen


class Data(Screen):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__(game_model)
        self.maze = Maze((19, 19), self.game_model.seed)
        self.maze.rect.topleft = (
            self.get_center(self.maze.rect.width),
            self.get_center(self.maze.rect.height, horizontal=False),
        )
        self.pacgums = Pacgums(self.maze.maze, self.game_model.points_per_pacgum, self.game_model.points_per_super_pacgum)
        self.pacgums.generate_gums(self.game_model.pacgum_number)
        self.player = Player(
                (9, 9), self.maze.maze, self.pacgums,
                self.game_model.life
            )
        self.ghosts = [
            Ghost((18, 18), self.maze.maze, "red", self.game_model.points_per_ghost),
            Ghost((0, 0), self.maze.maze, "blue", self.game_model.points_per_ghost),
            Ghost((18, 0),  self.maze.maze, "yellow", self.game_model.points_per_ghost),
            Ghost((0, 18),  self.maze.maze, "pink", self.game_model.points_per_ghost),
        ]
        self.buttons: dict[str, Any] = {}

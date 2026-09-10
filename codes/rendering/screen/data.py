from typing import Any

from codes.pacgums import Pacgum
from codes.pacgums.pacgum import SuperGum
from codes.parsing.parse import GameModel
from codes.players import Ghost, Player
from codes.rendering.component.maze import Maze
from codes.rendering.screen.base_screen import Screen
from codes.utilities import get_valid_gums_coord


class Data(Screen):
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


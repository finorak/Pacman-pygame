import random
from typing import Any

from codes.algorithm import Algorithm
from codes.setting import TARGET_DIRECTION
from codes.utilities import player_in_range, target_reached
from codes.utilities.utils import get_state

from ..component import AnimatedSprite
from ..utils import SpriteLoader
from .entity import Entity


class Ghost(Entity):
    def __init__(
        self, pos: tuple[int, int], maze: list[list[int]], name: str
    ) -> None:
        self.name = name
        super().__init__(pos, maze)
        self.algorithm = Algorithm()
        self._radius: int = 2 # cell to count just upgrade as level grow
        self._target_position = pos

    def load_image(self) -> dict[str, AnimatedSprite]:
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder(
                    "assets", "ghosts", self.name, direction
                ),
            )
        return result

    def _find_path(self, player: Any) -> str:
        next_dir = random.choice(['down', 'left', 'right', 'up'])
        if player_in_range(self.pos, player.pos, self._radius):
            paths = self.algorithm.bfs(self.pos, player.pos, self.maze)
            if not paths:
                return self.next_dir
            target_vec = get_state(paths[0], self.pos)
            state = TARGET_DIRECTION[target_vec]
            return state
        return next_dir

    def get_input(self, player: Any) -> None:
        """This one will be used to change the target
        of the ghost.
          .
        # player -> Player class
        """
        if self._is_moving:
            return
        self.next_dir = self._find_path(player)

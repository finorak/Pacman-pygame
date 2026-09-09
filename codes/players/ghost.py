import random
from typing import Any, ClassVar

from codes.algorithm import Algorithm
from codes.rendering.component import AnimatedSprite
from codes.rendering.utils import SpriteLoader
from codes.setting import TARGET_DIRECTION
from codes.utilities import player_in_range
from codes.utilities.utils import get_state

from .entity import Entity


class Ghost(Entity):
    CAN_BE_EATEN: ClassVar = False

    def __init__(
        self, pos: tuple[int, int], maze: list[list[int]], name: str
    ) -> None:
        self.name = name
        super().__init__(pos, maze)
        self.speed = 2.0
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
        # TODO: find why the ghost isn't moving
        # in the direction of the player even though
        # the algorithm seems right
        choices = ['down', 'left', 'right', 'up']
        next_dir = random.choice(choices)
        paths = self.algorithm.bfs(self.pos, player.pos, self.maze)
        if self.CAN_BE_EATEN:
            if not paths:
                return self.next_dir
            target_vec = get_state(paths[0], self.pos)
            state = TARGET_DIRECTION[target_vec]
            choices.remove(state)
            return random.choice(choices)
        if player_in_range(self.pos, player.pos, self._radius):
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
        if player.pos == self.pos:
            player._reset(True)
        if self._is_moving:
            return
        self.next_dir = self.OPPOSITE[self._find_path(player)]

    @classmethod
    def change_state(cls: Any) -> 'Ghost':
        cls.CAN_BE_EATEN = not cls.CAN_BE_EATEN
        return cls

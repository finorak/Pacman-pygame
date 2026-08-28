import random
from typing import Any

from pygame import Surface

from codes.setting import TARGET_DIRECTION
from codes.utilities import cell_is_valid

from .base import BasePlayer


class Ghost(BasePlayer):
    # When this is on, every
    # ghost can be eaten.
    CAN_BE_EATEN: bool = False

    def __init__(
            self, frames: dict[str, list[Surface]],
            pos: tuple[int, int], life: int
    ) -> None:
        super().__init__(frames, pos, life)
        self.speed = 130
        self._radius: int = 20
        # the target of the ghost
        self._target: tuple[int, int] = pos

    def draw(self, screen: Surface) -> None:
        # pygame.draw.circle(screen, "green", self.rect.topleft, self._radius, 20)
        screen.blit(self.image, self.rect)

    def _cell_reached(self) -> bool:
        return self._x == self._target[0] and self._y == self._target[1]

    def update(self, dt: float, maze: list[list[int]]) -> None:
        # TODO: update this function because it start to
        # be full of random things
        self.frame_update(dt)
        print("target", self._target)
        # moving in random direction
        if self._cell_reached():
            target = random.choice(list(TARGET_DIRECTION))
            dx, dy = target
            if not cell_is_valid(
                        (self._x, self._y),
                        (self._x + dx, self._y + dy),
                        maze
            ):
                return
            self._state = TARGET_DIRECTION[target]
            self._target = (self._x + dx, self._y + dy)
        self._update_position(dt)

    def reset(self, *arg: Any, **kwarg: Any) -> None:
        ...

    # UPdate state of all ghost, to can('t) be eaten.
    @classmethod
    def update_ghost_state(cls: Any) -> 'Ghost':
        Ghost.CAN_BE_EATEN = not Ghost.CAN_BE_EATEN
        return cls

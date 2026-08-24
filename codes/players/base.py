from abc import ABC, abstractmethod

from pygame import Surface

from ..setting import PLAYER_FRAME_SETTING


class BasePlayer(ABC):
    def __init__(
            self,
            frames: dict[str, list[Surface]],
            pos: tuple[int, int],
            life: int,
    ) -> None:
        super().__init__()
        # surface is where to place the player.
        self._state: str = "left"
        self._frames = frames
        self._life = life
        self._x, self._y = pos
        self._frame_index: float = 0
        self.image = frames[self._state][0].convert_alpha()
        self.rect = frames[self._state][0].get_rect(topleft=(0, 0))

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        self._state = value

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def life(self) -> int:
        return self._life

    @life.setter
    def life(self, value: int) -> None:
        self.life = value

    @property
    def frame_index(self) -> float:
        return self._frame_index

    @frame_index.setter
    def frame_index(self, value: float) -> None:
        self._frame_index = value

    @abstractmethod
    def draw(self, screen: Surface) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    def base_update(self, dt: float) -> None:
        self.frame_index += 7 * dt
        self.image = self._frames[self.state][
                int(self.frame_index) % len(
                    self._frames[self.state]
                    )
                ].convert_alpha()
        self.rect.x += PLAYER_FRAME_SETTING[self.state]['speed_x'] * dt
        self.rect.y += PLAYER_FRAME_SETTING[self.state]['speed_y'] * dt

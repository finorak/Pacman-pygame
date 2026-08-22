from abc import ABC, abstractmethod

from pygame import Surface


class BasePlayer(ABC):
    def __init__(
            self,
            frames: dict[str, list[Surface]],
            pos: tuple[int, int],
            life: int,
    ) -> None:
        super().__init__()
        # surface is where to place the player.
        self.frames = frames
        self._life = life
        self._x, self._y = pos
        self.current_frame_index: int = 0

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

    @abstractmethod
    def draw(self, screen: Surface) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

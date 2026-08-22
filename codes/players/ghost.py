from pygame import Surface
from .base import BasePlayer


class Ghost(BasePlayer):
    def __init__(
            self, frames: dict[str, list[Surface]], pos: tuple[int, int], life: int
            ) -> None:
        super().__init__(frames, pos, life)

    def draw(self, screen: Surface) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

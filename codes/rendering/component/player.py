"""
Here is my ideas on the pacman player.

First, the player should wander in the maze using index
Example:
the size of the maze is 32 * 32. The player position should go only
in 0 to 31 in both x and y

This is to make sure the player only go to the expected direction in the
expected time.
"""


from ..utils import SpriteLoader
from .sprite import AnimatedSprite


class Player:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.x = float(pos[0])
        self.y = float(pos[1])

        self.sprites = self.load_image()
        self.current_sprite =  self.sprites["down"]

    def move(self, dt: float) -> None:
        # should be 3 cell per second
        self.x += 3 * dt

    def load_image(self) -> dict[str, AnimatedSprite]:
        directions = {"down", "left", "right", "up"}
        result = {}
        for direction in directions:
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder("assets", "pacman", direction),
            )
        return result

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)

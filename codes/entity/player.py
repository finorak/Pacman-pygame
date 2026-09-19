"""Player module to manage player."""

import pygame
from pygame.key import ScancodeWrapper

from codes.entity.ghost import Ghost
from codes.pacgums.pacgums import Pacgums
from codes.rendering.component import AnimatedSprite
from codes.rendering.utils import SpriteLoader

from .entity import Entity


class Player(Entity):
    """Player class for managing pac-man."""

    def __init__(
        self,
        pos: tuple[int, int],
        maze: list[list[int]],
        gums: Pacgums,
        life: int,
        max_time: int,
    ) -> None:
        """Initialize a player class instance.

        Args:
            pos: the position of the player.
            maze: the current maze.
            gums: class containing all the gum the player \
can eat.
            life: the life of the player.
            max_time: how many time in seconds te player has to complete \
a level.
        """
        super().__init__(pos, maze, life)
        self.pacgums = gums
        self.can_eat_ghost: bool = False
        self.score: int = 0
        self.current_level: int = 1
        self._cheat_mode: bool = False

        self.max_time = max_time
        self.timer: float = max_time

        self.is_dead = False
        self.dead_timer = 0.0
        self.dead_max = 1.8
        self.level = 1

    def load_image(self) -> dict[str, AnimatedSprite]:
        """Load sprites images.

        The key for the sprite should always be "up", "down", "left", "right"
        to make the movement easier. We can also add another state as long as
        these keys is present.
        Returns:
            dict: The dictionnary containing the sprites.
        """
        result: dict[str, AnimatedSprite] = {}
        for direction in ("down", "left", "right", "up", "dead"):
            result[direction] = AnimatedSprite(
                (0, 0),
                SpriteLoader.import_folder("assets", "pacman", direction),
            )
        result["dead"].animation_speed = 6
        return result

    def get_input(self, key: ScancodeWrapper) -> str | None:
        """Get input from user.

        Args:
            player: the player
        """
        if self.is_dead:
            return None
        curr_pos = (
            round(self.render_x),
            round(self.render_y),
        )
        point = self.pacgums.eat(curr_pos)
        self.score += point
        if point == self.pacgums.super_pacgum_score:
            Ghost.update_ghost_state(True)
        if self.timer <= 0 or self.life <= 0:
            return "finished"
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.next_dir = "up"
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            self.next_dir = "down"
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.next_dir = "right"
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            self.next_dir = "left"
        return None

    def update(self, dt: float) -> None:
        """Update ghosts state after each reset.

        Args:
            value: the state for each ghost after updating \
the default value is `False`
        """
        if self.is_dead:
            self.dead_timer += dt
            self.current_sprite = self.sprites["dead"]
            if self.dead_timer > self.dead_max:
                self.is_dead = False
                self.dead_timer = 0.0
                self.reset(kill=True)
            self.current_sprite.animate(dt)
            return
        if not self.cheat_mode:
            self.timer -= dt
            if self.timer < 0:
                self.reset(True)
        return super().update(dt)

    def reset(self, kill: bool = False) -> None:
        """Reset the entity's information.

        Args:
            kill: wether diminue the entity's life or not.
        """
        super().reset(kill)
        if self.cheat_mode:
            self.speed = 5.0

    def new_game(self) -> None:
        """Start a new game."""
        self.timer = self.max_time
        self.score = 0
        self.current_level = 1
        self.cheat_mode = False
        self.reset()

    def dead(self) -> None:
        """Change player state to dead."""
        self.is_dead = True

    @property
    def cheat_mode(self) -> bool:
        """Get cheat mode value."""
        return self._cheat_mode

    @cheat_mode.setter
    def cheat_mode(self, value: bool = False) -> None:
        """Set cheat mode value."""
        self._cheat_mode = value
        self.speed = 5.0 if value else 3.5

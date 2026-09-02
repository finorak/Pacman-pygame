import pygame


class Sprite:
    def __init__(
        self,
        pos: tuple[float, float],
        sprite: pygame.Surface,
    ) -> None:
        self.image = sprite
        self.rect = self.image.get_frect(topleft=pos)

    @property
    def position(self) -> tuple[float, float]:
        return self.rect.topleft

    @position.setter
    def position(self, pos: tuple[float, float]) -> None:
        self.rect.topleft = pos


class AnimatedSprite(Sprite):
    def __init__(
        self,
        pos: tuple[float, float],
        sprites: list[pygame.Surface],
    ) -> None:
        self.sprites = sprites
        self.sprite_index = 0
        self.animation_speed = 6
        self.sprite_count = len(self.sprites)
        super().__init__(pos, sprites[0])

    def animate(self, dt: float) -> None:
        self.sprite_index += dt * self.animation_speed
        self.image = self.sprites[int(self.sprite_index) % self.sprite_count]

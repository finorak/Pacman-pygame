import pygame

from codes.rendering.component.sprite import AnimatedSprite


class Button:
    def __init__(
        self,
        pos: tuple[int, int],
        sprites: dict[str, AnimatedSprite],
        result: str,
    ) -> None:
        self.pos = pos
        self.sprites = sprites
        self.current_sprite = sprites["normal"]
        self.result = result

    def draw(self, screen: pygame.Surface) -> None:
        self.mouse_hover()
        screen.blit(self.current_sprite.image, self.pos)

    def mouse_hover(self):
        self.current_sprite = self.sprites["normal"]
        pos = pygame.mouse.get_pos()
        if self.current_sprite.rect.collidepoint(pos):
            self.current_sprite = self.sprites["hover"]

    def mouse_pressed(self) -> None:
        self.current_sprite = self.sprites["pressed"]

    def call_back(self) -> str:
        return self.result

    def update(self, dt: float) -> None:
        self.current_sprite.animate(dt)

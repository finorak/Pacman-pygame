import pygame

from codes.rendering.utils.sprite_loader import SpriteLoader


class Input:
    def __init__(
        self,
        pos: tuple[int, int],
        font: pygame.font.Font,
        placeholder: str = "",
    ) -> None:
        self.pos = pos
        self.font = font
        self.placeholder = placeholder
        self.background = SpriteLoader.import_image("assets", "hud", "input")
        self.rect = self.background.get_frect(topleft=pos)

        self.text = ""
        self.active = True

        self.timer = 0.0
        self.indicator = True

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.text = ""
            elif len(self.text) < 10 and (
                event.unicode.isalpha() or event.unicode == " "
            ):
                self.text += str(event.unicode)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, self.pos)
        text = self.text
        if self.indicator and self.active:
            text += "|"
        if not text and not self.active:
            text = self.placeholder
        if text:
            surface = self.font.render(text, True, (255, 255, 255))
            screen.blit(
                surface,
                (
                    self.rect.x + 20,
                    self.rect.centery - surface.get_height() // 2,
                ),
            )

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer > 0.5:
            self.indicator = not self.indicator
            self.timer = 0.0

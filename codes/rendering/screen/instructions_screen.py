import pygame

from codes.rendering.component.button import Button

from ..component import AnimatedSprite
from .base_screen import Screen


class InstructionsScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.assets = self.load_assets()
        self.buttons = {}
        self.load_buttons()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result

    def update(self, dt: float) -> None:
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.assets["logo"].image, self.assets["logo"].rect)
        for a in self.buttons.values():
            a.draw(screen)

    def load_assets(self) -> dict[str, AnimatedSprite]:
        image_path = {"logo": ("assets", "highscore", "Logo")}
        result = {}
        for name, path in image_path.items():
            result[name] = AnimatedSprite(
                (0, 0), [self.loader.import_image(*path)]
            )
        return result

    def load_buttons(self) -> None:
        buttons = {
            "exit": ((self.screen_size[0] - 60, 5), "Home"),
        }
        for button, (pos, result) in buttons.items():
            tmp = {}
            tmp["normal"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "l_buttons", button, "1")],
            )
            tmp["hover"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "l_buttons", button, "2")],
            )
            tmp["pressed"] = AnimatedSprite(
                pos,
                self.loader.import_folder("assets", "l_buttons", button),
            )
            a = Button(pos, tmp, result)
            self.buttons[button] = a

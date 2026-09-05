import pygame

from codes.rendering.component.sprite import Sprite

from ..component import AnimatedSprite, Button
from .base_screen import Screen


class HomeScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.assets: dict[str, AnimatedSprite] = {}
        self.buttons: dict[str, Button] = {}
        self.load_buttons()
        self.load_others()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result
        return None

    def update(self, dt: float) -> None:
        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.logo.image, self.logo.rect)
        for a in self.assets.values():
            screen.blit(a.image, a.rect)
        for a in self.buttons.values():
            a.draw(screen)

    def load_assets(self) -> dict[str, AnimatedSprite]:
        image_path = {"logo": ("assets", "Logo")}
        for name, path in image_path.items():
            self.assets[name] = AnimatedSprite(
                (0, 0), [self.loader.import_image(*path)]
            )
        return self.assets

    def load_buttons(self) -> None:
        buttons = {
            "start": ((220, 250), "Game"),
            "instructions": ((220, 310), "Instructions"),
            "highscore": ((220, 370), "HighScore"),
            "exit": ((220, 430), "exit"),
        }
        for button, (pos, result) in buttons.items():
            tmp = {}
            tmp["normal"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "button", button, "1")],
            )
            tmp["hover"] = AnimatedSprite(
                pos,
                [self.loader.import_image("assets", "button", button, "2")],
            )
            tmp["pressed"] = AnimatedSprite(
                pos,
                self.loader.import_folder("assets", "button", button),
            )
            a = Button(pos, tmp, result)
            self.buttons[button] = a

    def load_others(self) -> None:
        self.logo = Sprite(
            (0, 0),
            self.loader.import_image("assets", "Logo"),
        )

        self.logo.position = (
            75,
            30,
        )

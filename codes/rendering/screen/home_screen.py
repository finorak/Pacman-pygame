import pygame

from codes.rendering.component.sprite import Sprite

from ..component import AnimatedSprite, Button
from .base_screen import Screen


class HomeScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.assets: dict[str, AnimatedSprite] = {}
        self.buttons: dict[str, Button] = {}
        self.load_background()
        self.load_buttons()
        self.load_others()

    def get_input(self) -> None: ...

    def update(self, dt: float) -> None:
        self.background.rect.x -= 20 * dt
        for button in self.buttons.values():
            button.update(dt)


    def render(self, screen: pygame.Surface) -> None:
        self._render_background(screen)
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
        buttons = {"start": (220, 250), "exit": (220, 310)}
        for button, pos in buttons.items():
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
            a = Button(pos, tmp, button)
            self.buttons[button] = a

    def load_background(self) -> None:
        self.background = Sprite(
            (0, 0), self.loader.import_image("assets", "background")
        )
        print(self.background.rect.height)
        self.background.image = pygame.transform.scale2x(self.background.image)
        self.background.rect = self.background.image.get_frect()

    def load_others(self) -> None:
        self.logo = Sprite(
            (0, 0),
            self.loader.import_image("assets", "Logo"),
        )

        self.logo.position = (
            75,
            30,
        )

    def _render_background(self, screen: pygame.Surface) -> None:
        image_width = self.background.rect.width

        x = self.background.rect.x

        while x < self.screen_size[0]:
            screen.blit(self.background.image, (x, 0))
            x += image_width

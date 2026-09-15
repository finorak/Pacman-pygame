import pygame

from codes.data.data import Data
from codes.parsing.parse import GameModel
from codes.rendering.component.button import Button
from codes.rendering.component.sprite import AnimatedSprite
from codes.rendering.screen.base_screen import Screen
from codes.rendering.utils.sprite_loader import SpriteLoader


class PauseScreen(Screen):
    def __init__(self, game_model: GameModel, data: Data) -> None:
        super().__init__(game_model, data)
        self.background = SpriteLoader.import_image("assets", "hud", "table")
        self.background_rect = (
            self.get_center(self.background.width),
            self.get_center(self.background.height, horizontal=False) - 50,
        )
        self.buttons = {}
        self.load_buttons()
        self.logo = SpriteLoader.import_image("assets", "screen", "pause")

    def enter(self, screen: pygame.Surface) -> None:
        self.back = screen.copy()

    def get_input(self) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "Game"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for b in self.buttons.values():
                    if b.current_sprite.rect.collidepoint(pos):
                        return b.result
        return None

    def update(self, dt: float) -> None: ...

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.back)
        screen.blit(self.background, self.background_rect)
        screen.blit(self.logo, (self.get_center(self.logo.width, horizontal=True), 200))
        for button in self.buttons.values():
            button.draw(screen)

    def load_buttons(self) -> None:
        buttons = {
            "exit": ((self.screen_size[0] - 60, 5), "Home"),
            "home": (
                (self.get_center(47), self.get_center(52, horizontal=False)),
                "Home",
            ),
            "play": (
                (
                    self.get_center(47) + 120,
                    self.get_center(52, horizontal=False),
                ),
                "Game",
            ),
            "new": (
                (
                    self.get_center(47) - 120,
                    self.get_center(52, horizontal=False),
                ),
                "new",
            ),
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

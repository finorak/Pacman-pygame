import pygame


class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 950))
        pygame.display.set_caption("Pacman")

    def run(self) -> None:
        running: bool = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick() / 1000
            self.draw(dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            self.update(dt)

    def draw(self, dt: float) -> None:
        self.screen.fill("white")

    def update(self, dt: float) -> None:
        pygame.display.update()

from .base import Screen

class InstructionsScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def render(self) -> None:
        ...

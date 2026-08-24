from abc import ABC, abstractmethod

class Screen(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_input(self) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    @abstractmethod
    def render(self) -> None: ...

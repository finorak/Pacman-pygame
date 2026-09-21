"""Package that contains every screen for the program."""

from .base_screen import Screen
from .finished_screen import FinishedScreen
from .game_screen import GameScreen
from .highscore_screen import HighScoreScreen
from .home_screen import HomeScreen
from .instructions_screen import InstructionsScreen
from .pause_screen import PauseScreen

__all__ = [
    "FinishedScreen",
    "GameScreen",
    "HighScoreScreen",
    "HomeScreen",
    "InstructionsScreen",
    "PauseScreen",
    "Screen",
]

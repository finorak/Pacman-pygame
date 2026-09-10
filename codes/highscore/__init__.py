"""
Package containing the highscore module for the project.

It contains the various utils to read and save the highscore as well as
managing the highscores system.
"""

from .loader import HighScoreLoader
from .model import HighScoreModel

__all__ = ["HighScoreLoader", "HighScoreModel"]

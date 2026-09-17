"""High score loader module."""

import json
import sys
from pathlib import Path

from .model import HighScoreModel


class HighScoreLoader:
    """Class to load highscore."""

    def __init__(self, path: Path) -> None:
        """Initialize an `HighScoreLoader` instance.

        Args:
            path: the path of the highscore file.
        """
        self.path = path
        self.highscore = self.load()

        self.changed = True

    def load(self) -> list[HighScoreModel]:
        """Load highscore from path."""
        try:
            with open(self.path) as file:
                highscore = json.load(file)
            highscores = [
                HighScoreModel.model_validate(value) for value in highscore
            ]
            return sorted(highscores, key=lambda x: -x.player_score)[:10]
        except (OSError, ValueError) as e:
            print(
                f"[WARNING] Cannot load the save file {self.path}: {e}",
                file=sys.stderr,
            )
        return []

    def save(self, models: list[HighScoreModel]) -> None:
        """Save newly highscore into file.

        Args:
            models: all the highscore model.
        """
        with open(self.path, "w") as file:
            try:
                json.dump(
                    [model.model_dump() for model in models[:10]],
                    file,
                    indent=4,
                )
            except ValueError as e:
                print(
                        f"[WARNING] Cannot write the save file: {e}",
                        file=sys.stderr
                    )

    def add_score(self, name: str, score: int, time: int) -> None:
        """Add new score into database.

        Args:
            name: the name of the player.
            score: score gotten by the player.
            time: time elapsed to finish the game.
        """
        self.changed = True
        self.highscore.append(
            HighScoreModel(
                player_name=name, player_score=score, player_time=time
            )
        )
        self.highscore.sort(key=lambda x: -x.player_score)
        while len(self.highscore) > 10:
            self.highscore.pop()

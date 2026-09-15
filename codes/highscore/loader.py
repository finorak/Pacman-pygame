import json
from pathlib import Path

from .model import HighScoreModel


class HighScoreLoader:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.highscore = self.load()

    def load(self) -> list[HighScoreModel]:
        with open(self.path) as file:
            highscore = json.load(file)
        highscores = [
            HighScoreModel.model_validate(value) for value in highscore
        ]
        return sorted(highscores, key=lambda x: -x.player_score)[:10]

    def save(self, models: list[HighScoreModel]) -> None:
        with open(self.path, "w") as file:
            json.dump(
                [model.model_dump() for model in models[:10]],
                file,
                indent=4,
            )

    def update(self) -> None:
        self.highscore = sorted(
            self.highscore, key=lambda x: x.player_score, reverse=True
        )

    def add_score(self, name: str, score: int, time: int) -> None:
        self.highscore = sorted(
            self.highscore
            + [
                HighScoreModel(
                    player_name=name, player_score=score, player_time=time
                )
            ],
            key=lambda x: x.player_score,
            reverse=True,
        )[:10]

import json
from pathlib import Path

from .model import HighScoreModel


class HighScoreLoader:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[HighScoreModel]:
        with open(self.path) as file:
            highscore = json.load(file)
        return [HighScoreModel.model_validate(value) for value in highscore]

    def save(self, models: list[HighScoreModel]) -> None:
        with open(self.path, "w") as file:
            file.write(json.dumps([model.model_dump_json() for model in models]))

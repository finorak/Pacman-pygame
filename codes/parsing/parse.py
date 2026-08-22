import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ConfigError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GameModel(BaseModel):
    model_config = ConfigDict(extra="allow")
    config_path: str = Field(...)

    @model_validator(mode='after')
    def validate_model(self) -> 'GameModel':
        custom_data: list[str] = []
        try:
            with open(
                self.config_path, mode="r", encoding="utf-8"
            ) as file:
                lines = file.readlines()
        except Exception as e:
            raise ConfigError(e)
        for line in lines:
            stripped_line: str = line.strip()
            if stripped_line.startswith("#") or not stripped_line:
                continue
            custom_data.append(stripped_line)
        raw_json = "".join(custom_data).strip("[]")
        try:
            data = json.loads(raw_json)
        except Exception as e:
            raise ConfigError(e)
        self._create_attribute(data)
        if self.width <= 0 or self.height <= 0:
            raise ConfigError("Screen is too small.")
        if (
                self.pacgum_number <= 0
                or self.points_per_pacgum <= 0
                or self.points_per_ghost <= 0
                or self.player_life <= 0
                or self.seed <= 0
        ):
            raise ConfigError("No value can be less than or equal to 0.")
        return self

    def _create_attribute(self, data: Any) -> None:
        screen_setting = data.get("screen")
        game_setting = data.get("game_settng")
        self.levels = data.get("levels")
        if not screen_setting or not game_setting or self.levels is None:
            raise ConfigError("Mandatory key missing.")
        self._instance_checker(self.levels, list)
        self.width = screen_setting.get("width")
        self.height = screen_setting.get("height")
        self._instance_checker(self.width, int)
        self._instance_checker(self.height, int)
        pacgum_and_score = game_setting.get("pacgum_and_score")
        if pacgum_and_score is None:
            raise ConfigError("Pacgum and setting key missing or is equal to 0.")
        self.pacgum_number: int = pacgum_and_score.get("number")
        self._instance_checker(self.pacgum_number, int)
        self.points_per_pacgum: int = pacgum_and_score.get("points_per_pacgum")
        self._instance_checker(self.points_per_pacgum, int)
        self.points_per_ghost: int = pacgum_and_score.get("points_per_ghost")
        self._instance_checker(self.points_per_ghost, int)
        player = game_setting.get("player")
        if not player:
            raise ConfigError("Life key missing for player.")
        self.player_life = player.get("life")
        self._instance_checker(self.player_life, int)
        self.seed = game_setting.get("seed")
        self._instance_checker(self.seed, int)

    def _instance_checker(self, data: Any, obj: Any) -> None:
        if not isinstance(data, obj):
            raise ConfigError("Data type and value doesn't match.")

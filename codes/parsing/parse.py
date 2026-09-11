from pydantic import (
    BaseModel,
    Field,
)


class ConfigError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GameModel(BaseModel):
    pacgum_number: int = Field(ge=1, lt=50)
    points_per_pacgum: int = Field(ge=1)
    points_per_super_pacgum: int = Field(ge=1)
    points_per_ghost: int = Field(ge=1)
    level_max_time: int = Field(ge=5, le=90)
    life: int = Field(ge=3, le=10)
    seed: int = Field(default=42, ge=1)
    levels: list[list[int]] = Field(min_length=1)

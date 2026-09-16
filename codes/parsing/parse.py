from typing import Self

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


class ConfigError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GameModel(BaseModel):
    pacgum_number: int = Field(default=32)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=25)
    points_per_ghost: int = Field(default=100)
    level_max_time: int = Field(default=120)
    life: int = Field(default=3)
    seed: int = Field(default=42)
    level_count: int = Field(default=10)

    @model_validator(mode="after")
    def check_numbers(self) -> Self:
        if self.pacgum_number > 343 or self.pacgum_number <= 0:
            raise ValueError("Pacgum number must be between 343 and 1")
        if self.points_per_pacgum > 1000 or self.points_per_pacgum <= 0:
            raise ValueError("Pacgum point should be between 1000 and 1")
        if (
            self.points_per_super_pacgum > 1000
            or self.points_per_super_pacgum <= 0
        ):
            raise ValueError("Super pacgum point should be between 1000 and 1")
        # if self.level_max_time > 1000 or self.level_max_time <= 60:
        #     raise ValueError("Max time should be between 1000 and 60")
        if self.life > 10 or self.life <= 0:
            raise ValueError("Life count should be between 10 and 1")
        if self.level_count < 10:
            raise ValueError("Level count should be at least 10.")
        return self

from typing import Self

from pydantic import BaseModel, Field, model_validator


class HighScoreModel(BaseModel):
    player_name: str = Field(min_length=3, max_length=10)
    player_score: int = Field(ge=0)

    @model_validator(mode="after")
    def check_player_name(self) -> Self:
        if not self.player_name.isalnum():
            raise ValueError("Name can only be alphabet and space")
        return self

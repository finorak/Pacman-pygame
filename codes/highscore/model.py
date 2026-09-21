"""HighScoreModel model module."""

from typing import Self

from pydantic import BaseModel, Field, model_validator


class HighScoreModel(BaseModel):
    """Class to validate highscore content using pydantic.

    Args:
        player_name: the name of the player.
        player_score: the score of the player.
        player_time: time elapsed to finish game.
    """

    player_name: str = Field(min_length=3, max_length=10)
    player_score: int = Field(ge=0)
    player_time: int = Field(ge=0)

    @model_validator(mode="after")
    def check_player_name(self) -> Self:
        """Validate model."""
        if not self.player_name.replace(" ", "").isalnum():
            raise ValueError("Name can only be alphabet and space")
        return self

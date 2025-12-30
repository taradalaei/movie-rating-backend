from pydantic import BaseModel, validator


class RatingCreate(BaseModel):
    score: int

    @validator("score")
    def score_must_be_int_between_1_and_10(cls, v):
        # Match guide error message exactly
        if not isinstance(v, int) or v < 1 or v > 10:
            raise ValueError("Score must be an integer between 1 and 10")
        return v


class RatingCreated(BaseModel):
    id: int
    movie_id: int
    score: int

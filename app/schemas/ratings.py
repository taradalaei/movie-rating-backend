from pydantic import BaseModel, conint


class RatingCreate(BaseModel):
    score: conint(ge=1, le=10)


class RatingCreated(BaseModel):
    id: int
    movie_id: int
    score: int

from pydantic import BaseModel, conint, Field
from typing import List, Optional


class MovieCreate(BaseModel):
    title: str = Field(min_length=1)
    release_year: conint(ge=1800, le=2100)
    director_id: int
    genres: List[int] = Field(min_length=1)
    cast: Optional[str] = None


class MovieUpdate(BaseModel):
    title: str = Field(min_length=1)
    release_year: conint(ge=1800, le=2100)
    genres: List[int] = Field(min_length=1)
    cast: Optional[str] = None

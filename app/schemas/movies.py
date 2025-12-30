from pydantic import BaseModel
from typing import List, Optional


class DirectorMini(BaseModel):
    id: int
    name: str


class MovieListItem(BaseModel):
    id: int
    title: str
    release_year: int
    cast: Optional[str] = None
    director: DirectorMini
    genres: List[str]
    average_rating: Optional[float] = None
    ratings_count: int = 0

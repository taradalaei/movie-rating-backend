from pydantic import BaseModel
from typing import List, Optional


class DirectorDetail(BaseModel):
    id: int
    name: str
    birth_year: Optional[int] = None
    description: Optional[str] = None


class MovieDetail(BaseModel):
    id: int
    title: str
    release_year: int
    cast: Optional[str] = None
    director: DirectorDetail
    genres: List[str]
    ratings: List[int]
    average_rating: Optional[float] = None
    ratings_count: int

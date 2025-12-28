from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.common import SuccessResponse

from app.schemas.ratings import RatingCreate
from app.services.ratings_service import add_movie_rating

from app.services.movies_read_service import get_movies_paginated
from app.services.movies_search_service import search_movies_paginated
from app.services.movie_detail_service import get_movie_by_id

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.get("/search", response_model=SuccessResponse)
def search_movies_endpoint(
    q: Optional[str] = Query(default=None),
    director: Optional[str] = Query(default=None),
    genre: Optional[str] = Query(default=None),
    year_from: Optional[int] = Query(default=None, ge=1800),
    year_to: Optional[int] = Query(default=None, ge=1800),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = search_movies_paginated(
        db=db,
        q=q,
        director=director,
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        page=page,
        page_size=page_size,
    )
    return {"status": "success", "data": {"items": items}}


@router.get("", response_model=SuccessResponse)
def list_movies_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = get_movies_paginated(db, page=page, page_size=page_size)
    return {"status": "success", "data": {"items": items}}


@router.get("/{movie_id}", response_model=SuccessResponse)
def get_movie_detail_endpoint(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"status": "success", "data": movie}


@router.post("/{movie_id}/ratings", response_model=SuccessResponse)
def create_movie_rating_endpoint(
    movie_id: int,
    payload: RatingCreate,
    db: Session = Depends(get_db),
):
    result = add_movie_rating(db, movie_id=movie_id, score=payload.score)
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"status": "success", "data": result}

from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.common import SuccessResponse

from app.schemas.ratings import RatingCreate
from app.services.ratings_service import add_movie_rating

from app.services.movies_read_service import get_movies_paginated
from app.services.movies_search_service import search_movies_paginated
from app.services.movie_detail_service import get_movie_by_id
from fastapi.responses import JSONResponse
from app.schemas.movie_write import MovieCreate, MovieUpdate
from app.services.movies_write_service import (
    create_movie_service,
    update_movie_service,
    delete_movie_service,
)


router = APIRouter(prefix="/api/v1/movies", tags=["movies"])

def failure(code: int, message: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "failure",
            "error": {"code": code, "message": message},
        },
    )



@router.get("", response_model=SuccessResponse)
def list_movies_endpoint(
    title: Optional[str] = Query(default=None),
    release_year: Optional[int] = Query(default=None, ge=1800),
    genre: Optional[str] = Query(default=None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if release_year is not None and (release_year < 1888 or release_year > 2100):
        raise HTTPException(status_code=422, detail="Invalid release_year")

    if title is None and release_year is None and genre is None:
        items, total_items = get_movies_paginated(db, page=page, page_size=page_size)
    else:
        year_from = release_year
        year_to = release_year
        items, total_items = search_movies_paginated(
            db=db,
            q=title,
            director=None,
            genre=genre,
            year_from=year_from,
            year_to=year_to,
            page=page,
            page_size=page_size,
        )

    return {
        "status": "success",
        "data": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": (total_items + page_size - 1) // page_size if page_size else 0,
            "items": items,
        },
    }


@router.get("/{movie_id}", response_model=SuccessResponse)
def get_movie_detail_endpoint(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        return failure(404, "Movie not found", 404)
    return {"status": "success", "data": movie}


@router.post("/{movie_id}/ratings", response_model=SuccessResponse)
def create_movie_rating_endpoint(
    movie_id: int,
    payload: RatingCreate,
    db: Session = Depends(get_db),
):
    result = add_movie_rating(db, movie_id=movie_id, score=payload.score)
    if not result:
        return failure(404, "Movie not found", 404)

    return {"status": "success", "data": result}


@router.post("", response_model=SuccessResponse, status_code=201)
def create_movie_endpoint(payload: MovieCreate, db: Session = Depends(get_db)):
    movie = create_movie_service(db, payload)
    if movie is None:
        # مطابق مستند: Invalid director_id or genres => 422
        return failure(422, "Invalid director_id or genres", 422)

    return {"status": "success", "data": movie}


@router.put("/{movie_id}", response_model=SuccessResponse)
def update_movie_endpoint(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    result = update_movie_service(db, movie_id, payload)

    if result == "not_found":
        return failure(404, "Movie not found", 404)

    if result is None:
        return failure(422, "Invalid director_id or genres", 422)

    return {"status": "success", "data": result}


@router.delete("/{movie_id}", status_code=204)
def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    ok = delete_movie_service(db, movie_id)
    if not ok:
        return failure(404, "Movie not found", 404)
    return None

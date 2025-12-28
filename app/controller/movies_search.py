from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.movies_search_service import search_movies_paginated
from app.schemas.common import SuccessResponse

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

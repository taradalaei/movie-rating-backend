from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.movies_read_service import get_movies_paginated
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.get("", response_model=SuccessResponse)
def list_movies_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items = get_movies_paginated(db, page=page, page_size=page_size)
    return {"status": "success", "data": {"items": items}}

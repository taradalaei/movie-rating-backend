from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.movie_detail_service import get_movie_by_id
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/api/v1/movies", tags=["movies"])


@router.get("/{movie_id}", response_model=SuccessResponse)
def get_movie_detail_endpoint(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"status": "success", "data": movie}

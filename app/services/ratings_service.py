from sqlalchemy.orm import Session
from app.repositories.ratings_repository import create_rating
from app.schemas.ratings import RatingCreated


def add_movie_rating(db: Session, movie_id: int, score: int):
    result = create_rating(db, movie_id=movie_id, score=score)
    if not result:
        return None

    rating, avg_score, cnt = result

    return {
        "rating": RatingCreated(id=rating.id, movie_id=rating.movie_id, score=rating.score),
        "average_rating": float(avg_score) if avg_score is not None else None,
        "ratings_count": int(cnt) if cnt is not None else 0,
    }

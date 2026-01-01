import logging
from sqlalchemy.orm import Session

from app.repositories.ratings_repository import create_rating
from app.schemas.ratings import RatingCreated

logger = logging.getLogger(__name__)


def add_movie_rating(db: Session, movie_id: int, score: int):
    result = create_rating(db, movie_id=movie_id, score=score)
    if result is None:
        return None

    rating, avg_score, cnt = result

    return {
        "rating": RatingCreated(id=rating.id, movie_id=rating.movie_id, score=rating.score),
        "average_rating": float(avg_score) if avg_score is not None else None,
        "ratings_count": int(cnt) if cnt is not None else 0,
    }


def add_movie_rating_service(db: Session, movie_id: int, score: int):
    if not isinstance(score, int) or score < 1 or score > 10:
        logger.warning(
            "Invalid rating value (movie_id=%s, rating=%s, route=/api/v1/movies/%s/ratings)",
            movie_id,
            score,
            movie_id,
        )
        return "invalid_score"

    try:
        result = add_movie_rating(db, movie_id=movie_id, score=score)
    except Exception:
        logger.error(
            "Failed to save rating (movie_id=%s, rating=%s)",
            movie_id,
            score,
            exc_info=True,
        )
        return "error"

    if result is None:
        return None  # movie not found

    logger.info("Rating saved successfully (movie_id=%s, rating=%s)", movie_id, score)
    return result

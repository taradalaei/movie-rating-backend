from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.movie import Movie
from app.models.rating import MovieRating


def create_rating(db: Session, movie_id: int, score: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return None

    rating = MovieRating(movie_id=movie_id, score=score)
    db.add(rating)
    db.commit()
    db.refresh(rating)

    avg_cnt = (
        db.query(func.avg(MovieRating.score), func.count(MovieRating.id))
        .filter(MovieRating.movie_id == movie_id)
        .first()
    )

    return rating, avg_cnt[0], avg_cnt[1]

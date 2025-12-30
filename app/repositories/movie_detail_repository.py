from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.director import Director
from app.models.rating import MovieRating


def get_movie_detail(db: Session, movie_id: int):
    movie = (
        db.query(Movie)
        .join(Director)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not movie:
        return None

    ratings = (
        db.query(MovieRating.score)
        .filter(MovieRating.movie_id == movie_id)
        .all()
    )
    rating_values = [r[0] for r in ratings]

    avg_cnt = (
        db.query(
            func.avg(MovieRating.score),
            func.count(MovieRating.id),
        )
        .filter(MovieRating.movie_id == movie_id)
        .first()
    )

    avg_score = avg_cnt[0]
    count = avg_cnt[1]

    return movie, rating_values, avg_score, count

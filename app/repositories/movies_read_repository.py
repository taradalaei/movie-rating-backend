from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.director import Director
from app.models.rating import MovieRating


def list_movies(db: Session, offset: int, limit: int):
    agg = (
        db.query(
            MovieRating.movie_id.label("movie_id"),
            func.avg(MovieRating.score).label("avg_score"),
            func.count(MovieRating.id).label("cnt"),
        )
        .group_by(MovieRating.movie_id)
        .subquery()
    )

    rows = (
        db.query(Movie, Director, agg.c.avg_score, agg.c.cnt)
        .join(Director, Movie.director_id == Director.id)
        .outerjoin(agg, agg.c.movie_id == Movie.id)
        .order_by(Movie.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for movie, director, avg_score, cnt in rows:
        # movie.genres از relationship می‌آید
        genre_names = [g.name for g in movie.genres]
        result.append((movie, director, avg_score, cnt, genre_names))
    return result

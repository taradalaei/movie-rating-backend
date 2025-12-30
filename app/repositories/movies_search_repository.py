from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.movie import Movie
from app.models.director import Director
from app.models.genre import Genre
from app.models.rating import MovieRating


def search_movies(
    db: Session,
    q: Optional[str],
    director: Optional[str],
    genre: Optional[str],
    year_from: Optional[int],
    year_to: Optional[int],
    offset: int,
    limit: int,
):
    agg = (
        db.query(
            MovieRating.movie_id.label("movie_id"),
            func.avg(MovieRating.score).label("avg_score"),
            func.count(MovieRating.id).label("cnt"),
        )
        .group_by(MovieRating.movie_id)
        .subquery()
    )

    query = (
        db.query(Movie, Director, agg.c.avg_score, agg.c.cnt)
        .join(Director, Movie.director_id == Director.id)
        .outerjoin(agg, agg.c.movie_id == Movie.id)
    )

    if q:
        query = query.filter(Movie.title.ilike(f"%{q}%"))

    if director:
        query = query.filter(Director.name.ilike(f"%{director}%"))

    if year_from is not None:
        query = query.filter(Movie.release_year >= year_from)

    if year_to is not None:
        query = query.filter(Movie.release_year <= year_to)

    if genre:
        query = query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre}%")).distinct()

    rows = (
        query.order_by(Movie.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for movie, director_obj, avg_score, cnt in rows:
        genre_names = [g.name for g in movie.genres]
        result.append((movie, director_obj, avg_score, cnt, genre_names))
    return result

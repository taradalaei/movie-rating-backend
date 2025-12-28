from sqlalchemy.orm import Session
from app.repositories.movie_detail_repository import get_movie_detail
from app.schemas.movie_detail import MovieDetail, DirectorDetail


def get_movie_by_id(db: Session, movie_id: int):
    result = get_movie_detail(db, movie_id)

    if not result:
        return None

    movie, rating_values, avg_score, count = result

    return MovieDetail(
        id=movie.id,
        title=movie.title,
        release_year=movie.release_year,
        cast=getattr(movie, "cast", None),
        director=DirectorDetail(
            id=movie.director.id,
            name=movie.director.name,
            birth_year=movie.director.birth_year,
            description=movie.director.description,
        ),
        genres=[g.name for g in movie.genres],
        ratings=rating_values,
        average_rating=float(avg_score) if avg_score is not None else None,
        ratings_count=count,
    )

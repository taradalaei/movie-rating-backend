from sqlalchemy.orm import Session

from app.repositories.movies_write_repository import create_movie, update_movie, delete_movie
from app.schemas.movies import MovieListItem, DirectorMini


def _to_movie_item(movie):
    return MovieListItem(
        id=movie.id,
        title=movie.title,
        release_year=movie.release_year,
        cast=getattr(movie, "cast", None),
        director=DirectorMini(id=movie.director.id, name=movie.director.name),
        genres=[g.name for g in movie.genres],
        average_rating=None,
        ratings_count=0,
    )


def create_movie_service(db: Session, payload):
    movie = create_movie(
        db=db,
        title=payload.title,
        release_year=payload.release_year,
        cast=payload.cast,
        director_id=payload.director_id,
        genre_ids=payload.genres,
    )
    if movie is None:
        return None
    return _to_movie_item(movie)


def update_movie_service(db: Session, movie_id: int, payload):
    result = update_movie(
        db=db,
        movie_id=movie_id,
        title=payload.title,
        release_year=payload.release_year,
        cast=payload.cast,
        genre_ids=payload.genres,
    )
    if result == "not_found":
        return "not_found"
    if result is None:
        return None
    return _to_movie_item(result)


def delete_movie_service(db: Session, movie_id: int):
    return delete_movie(db, movie_id)

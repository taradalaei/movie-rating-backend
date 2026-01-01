from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.director import Director
from app.models.genre import Genre


def _get_director(db: Session, director_id: int):
    return db.query(Director).filter(Director.id == director_id).first()


def _get_genres_by_ids(db: Session, genre_ids: list[int]):
    genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
    return genres


def create_movie(
    db: Session,
    title: str,
    release_year: int,
    cast: str | None,
    director_id: int,
    genre_ids: list[int],
):
    director = _get_director(db, director_id)
    genres = _get_genres_by_ids(db, genre_ids)

    if (director is None) or (len(genres) != len(set(genre_ids))):
        return None

    movie = Movie(
        title=title,
        release_year=release_year,
        director_id=director_id,
        cast=cast,
    )
    movie.genres = genres

    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(
    db: Session,
    movie_id: int,
    title: str,
    release_year: int,
    cast: str | None,
    genre_ids: list[int],
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        return "not_found"

    genres = _get_genres_by_ids(db, genre_ids)
    if len(genres) != len(set(genre_ids)):
        return None

    movie.title = title
    movie.release_year = release_year
    movie.cast = cast

    movie.genres = genres

    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        return False

    db.delete(movie)
    db.commit()
    return True

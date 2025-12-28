from sqlalchemy.orm import Session
from app.repositories.movies_read_repository import list_movies
from app.schemas.movies import MovieListItem, DirectorMini


def get_movies_paginated(db: Session, page: int, page_size: int):
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10

    offset = (page - 1) * page_size
    rows = list_movies(db, offset=offset, limit=page_size)

    items = []
    for movie, director, avg_score, cnt, genre_names in rows:
        items.append(
            MovieListItem(
                id=movie.id,
                title=movie.title,
                release_year=movie.release_year,
                cast=getattr(movie, "cast", None),
                director=DirectorMini(id=director.id, name=director.name),
                genres=genre_names,
                average_rating=float(avg_score) if avg_score is not None else None,
                ratings_count=int(cnt) if cnt is not None else 0,
            )
        )
    return items

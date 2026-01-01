import logging
from sqlalchemy.orm import Session

from app.repositories.movies_read_repository import list_movies, count_movies
from app.schemas.movies import MovieListItem, DirectorMini

logger = logging.getLogger(__name__)


def get_movies_paginated(db: Session, page: int, page_size: int):
    """Return (items, total_items) for pagination metadata."""
    offset = (page - 1) * page_size

    rows = list_movies(db, offset=offset, limit=page_size)
    total_items = count_movies(db)

    items: list[MovieListItem] = []
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

    logger.info(
        "Movies listed successfully (route=/api/v1/movies, mode=read, page=%s, page_size=%s, returned=%s, total_items=%s)",
        page,
        page_size,
        len(items),
        total_items,
    )

    return items, total_items

from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.movies_search_repository import search_movies, count_search_movies
from app.schemas.movies import MovieListItem, DirectorMini


def search_movies_paginated(
    db: Session,
    q: Optional[str],
    director: Optional[str],
    genre: Optional[str],
    year_from: Optional[int],
    year_to: Optional[int],
    page: int,
    page_size: int,
):
    """Return (items, total_items) for pagination metadata."""
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10

    offset = (page - 1) * page_size

    total_items = count_search_movies(
        db=db, q=q, director=director, genre=genre, year_from=year_from, year_to=year_to
    )
    rows = search_movies(
        db=db,
        q=q,
        director=director,
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        offset=offset,
        limit=page_size,
    )

    items = []
    for movie, director_obj, avg_score, cnt, genre_names in rows:
        items.append(
            MovieListItem(
                id=movie.id,
                title=movie.title,
                release_year=movie.release_year,
                cast=getattr(movie, "cast", None),
                director=DirectorMini(id=director_obj.id, name=director_obj.name),
                genres=genre_names,
                average_rating=float(avg_score) if avg_score is not None else None,
                ratings_count=int(cnt) if cnt is not None else 0,
            )
        )
    return items, total_items

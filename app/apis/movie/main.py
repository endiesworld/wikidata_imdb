from typing import Optional

from app.models.core import IDModelMixin
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)
from app.models.domains.movie import NewMovie, Movie

from app.db.repositories import MoviesRepository

from . import crud

async def fn_create_movie(
    imdb_id: str,
    title: str,
    cost: int,
    icaa_rating: str,
    movies_repo: MoviesRepository,
    *,
    raise_duolicate_exception = False,
) -> IDModelMixin:
    movie = await crud.fn_get_movie_by_imdb(imdb_id=imdb_id, movies_repo=movies_repo)
    
    if movie:
        if raise_duolicate_exception:
            raise DuplicateDataException(
                current_record_id = movie.imdb_id, 
                message="A movie with this imdb value already exist")
            
        return None
    
    movie = NewMovie(imdb_id=imdb_id, title=title, cost=cost, icaa_rating=icaa_rating)
    
    return crud.fn_create_movie(movie=movie, movies_repo=movies_repo)
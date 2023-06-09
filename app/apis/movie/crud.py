from typing import List

from app.models.core import IDModelMixin
from app.models.domains.movie import NewMovie, Movie

from app.db.repositories import MoviesRepository


async def fn_create_movie(
    new_movie: NewMovie,
    movies_repo: MoviesRepository,
) -> IDModelMixin:
    return await movies_repo.create_movie(
        new_movie=new_movie,
    )
    
async def fn_get_movie_by_imdb(
    imdb_id: str,
    movies_repo: MoviesRepository,
) -> Movie:
    return await movies_repo.get_movie_imdb(
        imdb_id=imdb_id,
    )
    
async def fn_get_movies(movies_repo: MoviesRepository) -> List[Movie]:
        return await movies_repo.get_movies()
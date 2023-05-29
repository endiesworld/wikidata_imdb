from typing import Optional

from app.models.core import IDModelMixin
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)
from app.models.domains.genre import NewGenre, Genre

from app.db.repositories import GenresRepository

from . import crud

async def fn_create_genre(
    imdb_id: str,
    name: str,
    genres_repo: GenresRepository,
) -> IDModelMixin:
    
    new_genre = NewGenre(imdb_id=imdb_id, name=name,)
    return await crud.fn_create_genre( new_genre=new_genre, genres_repo=genres_repo)
    

fn_get_genre_by_imdb = crud.fn_get_genre_by_imdb
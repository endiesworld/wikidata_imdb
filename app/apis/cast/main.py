from typing import Optional

from app.models.core import IDModelMixin
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)
from app.models.domains.cast import NewCast, Cast

from app.db.repositories import CastsRepository

from . import crud

async def fn_create_cast(
    imdb_id: str,
    name: str,
    casts_repo: CastsRepository,
) -> IDModelMixin:
    
    new_cast = NewCast(imdb_id=imdb_id, name=name,)
    return await crud.fn_create_cast( new_cast, casts_repo=casts_repo)


fn_get_cast_by_imdb = crud.fn_get_cast_by_imdb
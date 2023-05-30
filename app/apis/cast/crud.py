from app.models.core import IDModelMixin
from app.models.domains.cast import NewCast, Cast

from app.db.repositories import CastsRepository


async def fn_create_cast(
    new_cast: NewCast,
    casts_repo: CastsRepository,
) -> IDModelMixin:
    return await casts_repo.create_cast(
        new_cast=new_cast,
    )
    
async def fn_get_cast_by_imdb(
    imdb_id: str,
    casts_repo: CastsRepository,
) -> Cast:
    return await casts_repo.get_cast_imdb(
        imdb_id=imdb_id,
    )
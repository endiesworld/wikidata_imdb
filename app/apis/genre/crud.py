from app.models.core import IDModelMixin
from app.models.domains.genre import NewGenre, Genre

from app.db.repositories import GenresRepository


async def fn_create_genre(
    new_genre: NewGenre,
    genres_repo: GenresRepository,
) -> IDModelMixin:
    return await genres_repo.create_genre(
        new_genre=new_genre,
    )
    
async def fn_get_genre_by_imdb(
    imdb_id: str,
    genres_repo: GenresRepository,
) -> Genre:
    return await genres_repo.get_genre_imdb(
        imdb_id=imdb_id,
    )
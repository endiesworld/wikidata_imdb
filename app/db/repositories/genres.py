from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.genre import (
    Genre,
    NewGenre,
)

NEW_GENRE_SQL = """
    INSERT INTO genres(imdb_id, genre)
    VALUES(:imdb_id, :genre)
    ON CONFLICT (imdb_id, genre) DO NOTHING
    RETURNING id;
"""

GET_GENRE_IMDB_SQL = """
    SELECT genre FROM genres WHERE imdb_id = :imdb_id;
"""

class GenresRepository(BaseRepository):
    async def create_genre(
        self, *, new_genre: NewGenre
    ) -> IDModelMixin:
        query_values = new_genre.dict()
        
        created_genre = await self.db.fetch_one(
            query=NEW_GENRE_SQL, values=query_values
        )
        return IDModelMixin(**created_genre)
    
    async def get_genre_imdb(
        self, *, imdb: str
    ) -> Genre:
        query_values = {"imdb": imdb}
        
        genre = await self.db.fetch_one(
            query=GET_GENRE_IMDB_SQL, values=query_values
        )
        return Genre(**genre)

    
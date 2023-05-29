from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.cast import (
    Cast,
    NewCast,
)

NEW_CAST_SQL = """
    INSERT INTO casts(imdb_id, name)
    VALUES(:imdb_id, :name)
    ON CONFLICT (imdb_id, name) DO NOTHING
    RETURNING id;
"""

GET_CAST_IMDB_SQL = """
    SELECT name FROM casts WHERE imdb_id = :imdb_id;
"""

class CastsRepository(BaseRepository):
    async def create_cast(
        self, *, new_cast: NewCast
    ) -> IDModelMixin:
        query_values = new_cast.dict()
        
        created_cast = await self.db.fetch_one(
            query=NEW_CAST_SQL, values=query_values
        )
        return IDModelMixin(**created_cast)
    
    async def get_cast_imdb(
        self, *, imdb: str
    ) -> Cast:
        query_values = {"imdb": imdb}
        
        cast = await self.db.fetch_one(
            query=GET_CAST_IMDB_SQL, values=query_values
        )
        return Cast(**cast)

    
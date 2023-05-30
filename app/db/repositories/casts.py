from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.cast import (
    Cast,
    NewCast,
    CastDBModel
)

NEW_CAST_SQL = """
    INSERT INTO casts(imdb_id, name)
    VALUES(:imdb_id, :name)
    ON CONFLICT (imdb_id, name) DO NOTHING
    RETURNING *;
"""

GET_CAST_IMDB_SQL = """
    SELECT imdb_id, name FROM casts WHERE imdb_id = :imdb_id;
"""

class CastsRepository(BaseRepository):
    async def create_cast(
        self, *, new_cast: NewCast
    ) -> CastDBModel:
        query_values = new_cast.dict()
        
        created_cast = await self.db.fetch_one(
            query=NEW_CAST_SQL, values=query_values
        )
        return CastDBModel(**created_cast) if created_cast else None
    
    async def get_cast_imdb(
        self, *, imdb_id: str
    ) -> List[Cast]:
        query_values = {"imdb_id": imdb_id}
        
        casts = await self.db.fetch_all(
            query=GET_CAST_IMDB_SQL, values=query_values
        )
        movie_casts = [Cast(**cast) for cast in casts] if casts else []
        return movie_casts

    
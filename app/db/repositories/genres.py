from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.genre import (
    Genre,
    NewGenre,
    GenreDBModel
)

NEW_GENRE_SQL = """
    INSERT INTO genres(imdb_id, genre)
    VALUES(:imdb_id, :genre)
    ON CONFLICT (imdb_id, genre) DO NOTHING
    RETURNING *;
"""

GET_GENRE_IMDB_SQL = """
    SELECT imdb_id, genre FROM genres WHERE imdb_id = :imdb_id;
"""

class GenresRepository(BaseRepository):
    async def create_genre(
        self, *, new_genre: NewGenre
    ) -> GenreDBModel:
        query_values = new_genre.dict()
        
        created_genre = await self.db.fetch_one(
            query=NEW_GENRE_SQL, values=query_values
        )
        return GenreDBModel(**created_genre) if created_genre else None
    
    async def get_genre_imdb(
        self, *, imdb_id: str
    ) -> List[Genre]:
        query_values = {"imdb_id": imdb_id}
        
        genres = await self.db.fetch_all(
            query=GET_GENRE_IMDB_SQL, values=query_values
        )
        movie_genres = [Genre(**genre) for genre in genres] if genres else []
        return movie_genres

    
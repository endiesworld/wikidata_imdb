import uuid
from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
from app.models.domains.movie import (
    Movie,
    NewMovie,
)

NEW_MOVIE_SQL = """
    INSERT INTO movies(imdb_id, title, cost, icaa_rating)
    VALUES(:imdb_id, :title, :cost, :icaa_rating)
    RETURNING id;
"""

GET_MOVIE_IMDB_SQL = """
    SELECT imdb_id, title, cost,icaa_rating FROM movies WHERE imdb_id = :imdb_id;
"""

class MoviesRepository(BaseRepository):
    async def create_movie(
        self, *, new_movie: NewMovie
    ) -> IDModelMixin:
        query_values = new_movie.dict()
        
        created_movie = await self.db.fetch_one(
            query=NEW_MOVIE_SQL, values=query_values
        )
        return IDModelMixin(**created_movie)
    
    async def get_movie_imdb(
        self, *, imdb: str
    ) -> Movie:
        query_values = {"imdb": imdb}
        
        movie = await self.db.fetch_one(
            query=GET_MOVIE_IMDB_SQL, values=query_values
        )
        return Movie(**movie)

    
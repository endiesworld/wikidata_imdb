from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import DeletedCount, IDModelMixin, RecordStatus, UpdatedRecord
from app.models.domains.movie import (
    Movie,
    NewMovie,
    MovieDBModel
)

NEW_MOVIE_SQL = """
    INSERT INTO movies(imdb_id, title, icaa_rating)
    VALUES(:imdb_id, :title, :icaa_rating)
    RETURNING *;
"""

GET_MOVIES_SQL = """
    SELECT imdb_id, title, icaa_rating FROM movies;
"""

GET_MOVIE_IMDB_SQL = """
    SELECT imdb_id, title, icaa_rating FROM movies WHERE imdb_id = :imdb_id;
"""

class MoviesRepository(BaseRepository):
    async def create_movie(
        self, *, new_movie: NewMovie
    ) -> MovieDBModel:
        query_values = new_movie.dict()
        
        created_movie = await self.db.fetch_one(
            query=NEW_MOVIE_SQL, values=query_values
        )
        return MovieDBModel(**created_movie)
    
    async def get_movie_imdb(
        self, *, imdb_id: str
    ) -> Movie:
        query_values = {"imdb_id": imdb_id}
        
        movie = await self.db.fetch_one(
            query=GET_MOVIE_IMDB_SQL, values=query_values
        )
        return Movie(**movie) if movie else None
    
    async def get_movies(
        self
    ) -> List[Movie]:
        movies = await self.db.fetch_all(
            query=GET_MOVIES_SQL
        )
        movies_ = [Movie(**movie) for movie in movies] if movies else []
        return movies_

    
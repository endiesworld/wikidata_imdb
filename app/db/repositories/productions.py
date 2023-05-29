from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.production import (
    Production,
    NewProduction,
)


NEW_PRODUCTION_SQL = """
    INSERT INTO productions(imdb_id, director, country, producer, language, company, cost, date)
    VALUES(:imdb_id, :director, :country, :producer, :language, :company, :cost, :date)
    ON CONFLICT (imdb_id, director, country, producer, language, company, cost, date) DO NOTHING
    RETURNING id;
"""

GET_PRODUCTION_IMDB_SQL = """
    SELECT director, country, producer, language, company, cost, date FROM productions WHERE imdb_id = :imdb_id;
"""

class ProductionsRepository(BaseRepository):
    async def create_production(
        self, *, new_production: NewProduction
    ) -> IDModelMixin:
        query_values = new_production.dict()
        
        created_production = await self.db.fetch_one(
            query=NEW_PRODUCTION_SQL, values=query_values
        )
        return IDModelMixin(**created_production)
    
    async def get_production_imdb(
        self, *, imdb: str
    ) -> Production:
        query_values = {"imdb": imdb}
        
        production = await self.db.fetch_one(
            query=GET_PRODUCTION_IMDB_SQL, values=query_values
        )
        return Production(**production)

    
from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.production import (
    Production,
    NewProduction,
    ProductionDBModel
)


NEW_PRODUCTION_SQL = """
    INSERT INTO productions(imdb_id, director, country, producer, language, duration, distributor, company, cost, date)
    VALUES(:imdb_id, :director, :country, :producer, :language, :duration, :distributor, :company, :cost, :date)
    ON CONFLICT (imdb_id, director, country, producer, language, duration, distributor, company, cost, date) DO NOTHING
    RETURNING *;
"""

GET_PRODUCTION_IMDB_SQL = """
    SELECT imdb_id, director, country, producer, language, duration, distributor, company, cost, date FROM productions WHERE imdb_id = :imdb_id;
"""

class ProductionsRepository(BaseRepository):
    async def create_production(
        self, *, new_production: NewProduction
    ) -> ProductionDBModel:
        query_values = new_production.dict()
        
        created_production = await self.db.fetch_one(
            query=NEW_PRODUCTION_SQL, values=query_values
        )
        return ProductionDBModel(**created_production) if created_production else None
    
    async def get_production_imdb(
        self, *, imdb_id: str
    ) -> List[Production]:
        query_values = {"imdb_id": imdb_id}
        
        productions = await self.db.fetch_all(
            query=GET_PRODUCTION_IMDB_SQL, values=query_values
        )
        movie_productions = (
            [Production(**production) for production in productions] 
            if productions else []
        )
        return movie_productions

    
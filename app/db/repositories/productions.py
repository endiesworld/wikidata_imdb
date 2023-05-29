from typing import List, Optional

from app.db.base import BaseRepository
from app.models.core import  IDModelMixin
from app.models.domains.production_company import (
    ProductionCompany,
    NewProductionCompany,
)

NEW_PRODUCTION_COMPANY_SQL = """
    INSERT INTO production_companies(imdb_id, name)
    VALUES(:imdb_id, :name)
    RETURNING id;
"""

GET_PRODUCTION_COMPANY_IMDB_SQL = """
    SELECT name FROM production_companies WHERE imdb_id = :imdb_id;
"""

class ProductionCompanysRepository(BaseRepository):
    async def create_production_company(
        self, *, new_production_company: NewProductionCompany
    ) -> IDModelMixin:
        query_values = new_production_company.dict()
        
        created_production_company = await self.db.fetch_one(
            query=NEW_PRODUCTION_COMPANY_SQL, values=query_values
        )
        return IDModelMixin(**created_production_company)
    
    async def get_production_company_imdb(
        self, *, imdb: str
    ) -> ProductionCompany:
        query_values = {"imdb": imdb}
        
        production_company = await self.db.fetch_one(
            query=GET_PRODUCTION_COMPANY_IMDB_SQL, values=query_values
        )
        return ProductionCompany(**production_company)

    
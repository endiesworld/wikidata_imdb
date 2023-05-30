from typing import Optional

from app.models.core import IDModelMixin
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)
from app.models.domains.production import NewProduction, Production

from app.db.repositories import ProductionsRepository

from . import crud

async def fn_create_production(
    imdb_id: str,
    director: str,
    country: int,
    duration: str,
    producer: str,
    language: str,
    distributor: str,
    company: int,
    cost: int,
    date: str,
    productions_repo: ProductionsRepository,
) -> IDModelMixin:
    
    new_production = NewProduction(
        imdb_id=imdb_id, 
        director=director, 
        country=country, 
        duration=duration,
        producer=producer,
        language=language, 
        distributor=distributor, 
        cost=cost, 
        company=company,
        date=date
        )
    
    return await crud.fn_create_production(new_production=new_production, productions_repo=productions_repo)


fn_get_production_by_imdb = crud.fn_get_production_by_imdb
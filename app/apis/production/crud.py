from app.models.core import IDModelMixin
from app.models.domains.production import NewProduction, Production

from app.db.repositories import ProductionsRepository


async def fn_create_production(
    new_production: NewProduction,
    productions_repo: ProductionsRepository,
) -> IDModelMixin:
    return await productions_repo.create_production(
        new_production=new_production,
    )
    
async def fn_get_production_by_imdb(
    imdb_id: str,
    productions_repo: ProductionsRepository,
) -> Production:
    return await productions_repo.get_production_imdb(
        imdb_id=imdb_id,
    )
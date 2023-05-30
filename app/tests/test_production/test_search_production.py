import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.production.crud import fn_create_production, fn_get_production_by_imdb
from app.apis.movie.crud import fn_create_movie
from app.db.repositories import ProductionsRepository, MoviesRepository

from app.models.domains.production import NewProduction, Production
from app.models.domains.movie import NewMovie
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_production_by_imdb


@pytest_asyncio.fixture(scope="class")
def new_production() -> NewProduction:
    return fixed_data.new_production()

@pytest_asyncio.fixture(scope="class")
def new_movie() -> NewMovie:
    return fixed_data.new_movie()


@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    productions_repo: ProductionsRepository,
    new_production: NewProduction,
    new_movie: NewMovie,
    movies_repo: MoviesRepository,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE productions CASCADE")
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")

    async def do_setup():
        _ = await fn_create_movie(
            new_movie,
            movies_repo,
        )
        movie_production = await fn_create_production(
            new_production,
            productions_repo,
        )
        return {
            "new_production": new_production,
            "imdb_id": movie_production.imdb_id,
            }

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestSearchProduction:
    async def test_setup(self, setup):
        new_production = setup["new_production"]
        imdb_id = setup["imdb_id"]

        assert isinstance(new_production, NewProduction)
        assert isinstance(imdb_id, str)
        
    async def test_search_production(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        productions_repo: ProductionsRepository,
        setup
    ) -> None:
        new_production = setup["new_production"]
        imdb_id = setup["imdb_id"]
        
        test_results = await FUNCTION_TO_TEST(
            imdb_id,
            productions_repo,
        )
        
        assert len(test_results) == 1
        assert isinstance(test_results[0], Production)
        assert test_results[0].imdb_id is not None
        assert test_results[0].director == new_production.director
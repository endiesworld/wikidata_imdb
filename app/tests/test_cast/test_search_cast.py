import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.apis.cast.crud import fn_create_cast, fn_get_cast_by_imdb
from app.db.repositories import CastsRepository

from app.models.domains.cast import NewCast, Cast
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_cast_by_imdb


@pytest_asyncio.fixture(scope="class")
def new_cast() -> NewCast:
    return fixed_data.new_cast()


@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    casts_repo: CastsRepository,
    new_cast: NewCast,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE casts CASCADE")

    async def do_setup():
        movie_cast = await fn_create_cast(
            new_cast,
            casts_repo,
        )
        return {
            "new_cast": new_cast,
            "imdb_id": movie_cast.imdb_id,
            }

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestSearchCast:
    async def test_setup(self, setup):
        new_cast = setup["new_cast"]
        imdb_id = setup["imdb_id"]

        assert isinstance(new_cast, NewCast)
        assert isinstance(imdb_id, str)
        
    async def test_search_cast(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        casts_repo: CastsRepository,
        setup
    ) -> None:
        new_cast = setup["new_cast"]
        imdb_id = setup["imdb_id"]
        
        test_results = await FUNCTION_TO_TEST(
            imdb_id,
            casts_repo,
        )
        
        assert len(test_results) == 1
        assert isinstance(test_results[0], Cast)
        assert test_results[0].imdb_id is not None
        assert test_results[0].name == new_cast.name
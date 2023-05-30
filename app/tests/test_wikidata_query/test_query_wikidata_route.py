import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

@pytest_asyncio.fixture(scope="class")
async def setup(
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE casts CASCADE")
        await db.fetch_one("TRUNCATE TABLE movies CASCADE")
        await db.fetch_one("TRUNCATE TABLE productions CASCADE")
        await db.fetch_one("TRUNCATE TABLE reviews CASCADE")
        await db.fetch_one("TRUNCATE TABLE genres CASCADE")

    async def do_setup():
        # To put any necessary setup here
        ...

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestLoadWikidata:
    
    async def test_load_wikidata(
        self, app: FastAPI, platform_client: AsyncClient, setup
    ) -> None:
        
        res = await platform_client.post(
            "/query/wikidata/movies",
        )
        res_body = res.json()

        assert res.status_code == status.HTTP_201_CREATED
        assert res_body['details'] == 'Movies laoded from wikidata successfully'
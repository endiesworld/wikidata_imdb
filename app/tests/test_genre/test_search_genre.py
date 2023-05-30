import pytest
import pytest_asyncio
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient

from app.apis.genre.crud import fn_create_genre, fn_get_genre_by_imdb
from app.db.repositories import GenresRepository

from app.models.domains.genre import NewGenre, Genre
from app.tests.helpers import fixed_data

pytestmark = pytest.mark.asyncio

FUNCTION_TO_TEST = fn_get_genre_by_imdb


@pytest_asyncio.fixture(scope="class")
def new_genre() -> NewGenre:
    return fixed_data.new_genre()


@pytest_asyncio.fixture(scope="class")
async def setup(
    app: FastAPI,
    platform_client: AsyncClient,
    genres_repo: GenresRepository,
    new_genre: NewGenre,
    db: Database,
):
    async def do_teardown():
        await db.fetch_one("TRUNCATE TABLE genres CASCADE")

    async def do_setup():
        movie_genre = await fn_create_genre(
            new_genre,
            genres_repo,
        )
        return {
            "new_genre": new_genre,
            "imdb_id": movie_genre.imdb_id,
            }

    await do_teardown()
    yield await do_setup()
    await do_teardown()
    
    
class TestSearchGenre:
    async def test_setup(self, setup):
        new_genre = setup["new_genre"]
        imdb_id = setup["imdb_id"]

        assert isinstance(new_genre, NewGenre)
        assert isinstance(imdb_id, str)
        
    async def test_search_genre(
        self, 
        app: FastAPI, 
        platform_client: AsyncClient, 
        genres_repo: GenresRepository,
        setup
    ) -> None:
        new_genre = setup["new_genre"]
        imdb_id = setup["imdb_id"]
        
        test_results = await FUNCTION_TO_TEST(
            imdb_id,
            genres_repo,
        )
        
        assert len(test_results) == 1
        assert isinstance(test_results[0], Genre)
        assert test_results[0].imdb_id is not None
        assert test_results[0].genre == new_genre.genre
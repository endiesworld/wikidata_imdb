from typing import Any, Optional

from fastapi import APIRouter, Depends, Request, status

from app.apis.wikidata import fn_query_wikidata_movies
from app.db.dependency import get_repository
from app.models.domains.movie import Movie
from app.models.exceptions.crud_exception import NotFoundError

from app.db.repositories import MoviesRepository
from app.db.repositories import GenresRepository
from app.db.repositories import ProductionsRepository
from app.db.repositories import ReviewsRepository

router = APIRouter()

# To include query limit
@router.post(
    "/query/wikidata/movies",
    tags=["wikidata-movies"],
    name="20000:Entries:wikidata:movies:create",
    operation_id="wikidata_movies_create",
    responses={
        status.HTTP_201_CREATED: {"model": Movie},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
    status_code=status.HTTP_201_CREATED,
)
async def query_wikidata_movies(
    request: Request,
    movies_repo: MoviesRepository= Depends(
        get_repository(MoviesRepository)
    ),
    genres_repo: GenresRepository= Depends(
        get_repository(GenresRepository)
    ),
    productions_repo: ProductionsRepository= Depends(
        get_repository(ProductionsRepository)
    ),
    reviews_repo: ReviewsRepository= Depends(
        get_repository(ReviewsRepository)
    ),
    
)->Any:
    
    return await fn_query_wikidata_movies(
        movies_repo=movies_repo,
        genres_repo=genres_repo,
        productions_repo=productions_repo,
        reviews_repo=reviews_repo,
    )
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Request, status

from app.apis.movie import fn_get_movies, fn_get_movie_details
from app.db.dependency import get_repository
from app.models.domains.movie import Movie
from app.models.domains.movie_details import MovieDetails
from app.models.exceptions.crud_exception import NotFoundError

from app.db.repositories import MoviesRepository
from app.db.repositories import GenresRepository
from app.db.repositories import ProductionsRepository
from app.db.repositories import ReviewsRepository

router = APIRouter()


@router.get(
    "/movies",
    tags=["movies"],
    name="movies:get",
    operation_id="movies_get",
    responses={
        status.HTTP_200_OK: {"model": Movie},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def get_movies(
    request: Request,
    movies_repo: MoviesRepository= Depends(
        get_repository(MoviesRepository)
    ),
)->List[Movie]:
    return await fn_get_movies(
        movies_repo=movies_repo,
    )
    

@router.get(
    "/movies/imdb/{imdb_id}",
    tags=["movies"],
    name="movies:imdb:get",
    operation_id="movies_imdb_get",
    responses={
        status.HTTP_200_OK: {"model": MovieDetails},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundError},
    },
)
async def get_movie_details(
    request: Request,
    imdb_id: str,
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
)->Optional[MovieDetails]:
    return await fn_get_movie_details(
        imdb_id, movies_repo, genres_repo, productions_repo, reviews_repo
    )
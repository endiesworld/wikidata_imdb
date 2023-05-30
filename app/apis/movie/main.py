from typing import Optional

from app.models.core import IDModelMixin
from app.models.exceptions.crud_exception import (
    NotFoundException,
    DuplicateDataException,
)
from app.models.domains.movie import NewMovie, Movie
from app.models.domains.movie_details import MovieDetails

from app.db.repositories import MoviesRepository
from app.db.repositories import GenresRepository
from app.db.repositories import ProductionsRepository
from app.db.repositories import ReviewsRepository

from app.apis.genre import fn_get_genre_by_imdb
from app.apis.production import fn_get_production_by_imdb
from app.apis.review import fn_get_review_by_imdb

from . import crud

async def fn_create_movie(
    imdb_id: str,
    title: str,
    icaa_rating: str,
    movies_repo: MoviesRepository,
    *,
    raise_duolicate_exception = False,
) -> IDModelMixin:
    movie = await crud.fn_get_movie_by_imdb(imdb_id=imdb_id, movies_repo=movies_repo)
    
    if movie:
        if raise_duolicate_exception:
            raise DuplicateDataException(
                current_record_id = movie.imdb_id, 
                message="A movie with this imdb value already exist")
            
        return None
    
    new_movie = NewMovie(imdb_id=imdb_id, title=title, icaa_rating=icaa_rating)
    
    return await crud.fn_create_movie(new_movie=new_movie, movies_repo=movies_repo)


fn_get_movie_by_imdb =  crud.fn_get_movie_by_imdb


async def fn_get_movie_details(
        imdb_id: str,
        movies_repo: MoviesRepository,
        genres_repo: GenresRepository,
        productions_repo: ProductionsRepository,
        reviews_repo: ReviewsRepository,
    )-> Optional[MovieDetails]:
    
    movie = await fn_get_movie_by_imdb(imdb_id, movies_repo)
    
    if movie is None:
        raise NotFoundException(message="Movie not found.")
    
    genre = await fn_get_genre_by_imdb(imdb_id, genres_repo)
    production = await fn_get_production_by_imdb(imdb_id, productions_repo)
    review = await fn_get_review_by_imdb(imdb_id, reviews_repo)
    
    movie_details = MovieDetails(
        imdb_id=movie.imdb_id, 
        title=movie.title,
        icaa_rating=movie.icaa_rating,
        genre=genre,
        production=production,
        review=review
    )
    
    return movie_details
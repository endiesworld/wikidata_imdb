from typing import Optional

from fastapi import status
from SPARQLWrapper import SPARQLWrapper, JSON
from app.models.core import StatusResponse

from app.apis.movie import fn_create_movie
from app.apis.production import fn_create_production
from app.apis.genre import fn_create_genre
from app.apis.review import fn_create_review

from app.db.repositories import MoviesRepository
from app.db.repositories import GenresRepository
from app.db.repositories import ProductionsRepository
from app.db.repositories import ReviewsRepository



# Set up the SPARQL endpoint URL
sparql_endpoint = "https://query.wikidata.org/sparql"

# Create a SPARQLWrapper object and set the endpoint URL
sparql = SPARQLWrapper(sparql_endpoint)

# Set the SPARQL query
FETCH_MOVIE_DATA_SPARQL = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?imdbId ?title ?publicationDate ?producerLabel ?genreLabel ?directorLabel ?countryLabel ?languageLabel ?production_companyLabel ?distributorLabel ?durationLabel ?reviewLabel ?costLabel ?icaa_ratingLabel
WHERE {
        ?movie wdt:P31 wd:Q11424;
        wdt:P1476 ?title;
        wdt:P136 ?genre;
        wdt:P495 ?country;
        wdt:P364 ?original_language;
        wdt:P57 ?director;
        wdt:P58 ?screen_writer;
        wdt:P162 ?producer;
        wdt:P272 ?production_company;
        wdt:P750 ?distributor;
        wdt:P2047 ?duration;
        wdt:P444 ?review;
        wdt:P2130 ?cost;
        wdt:P3306 ?icaa_rating;
        wdt:P577 ?publicationDate;
        wdt:P345 ?imdbId.

    FILTER (YEAR(?publicationDate) > 2013)
    SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
    ?genre rdfs:label ?genreLabel.
    ?director rdfs:label ?directorLabel.
    ?country rdfs:label ?countryLabel.
    ?producer rdfs:label ?producerLabel.
    ?screen_writer rdfs:label ?screen_writerLabel.
    ?original_language rdfs:label ?languageLabel.
    ?production_company rdfs:label ?production_companyLabel.
    ?distributor rdfs:label ?distributorLabel.
    ?duration rdfs:label ?durationLabel.
    ?review rdfs:label ?reviewLabel.
    ?cost rdfs:label ?costLabel.
    ?icaa_rating rdfs:label ?icaa_ratingLabel.
  }
}
LIMIT 3
"""

async def fn_query_wikidata_movies(
    movies_repo: MoviesRepository,
    genres_repo: GenresRepository,
    productions_repo: ProductionsRepository,
    reviews_repo: ReviewsRepository,
) :
    # Set the query and response format
    sparql.setQuery(FETCH_MOVIE_DATA_SPARQL)
    sparql.setReturnFormat(JSON)

    # Execute the SPARQL query and get the results
    results = sparql.query().convert()

    # Process the results
    for result in results["results"]["bindings"]:
        imdb_id = result["imdbId"]["value"]
        title = result["title"]["value"]
        country = result["countryLabel"]["value"]
        date = result["publicationDate"]["value"]
        language = result["languageLabel"]["value"]
        cost = result["costLabel"]["value"]
        genre = result["genreLabel"]["value"]
        director = result["directorLabel"]["value"]
        producer = result["producerLabel"]["value"]
        company = result["production_companyLabel"]["value"]
        distributor = result["distributorLabel"]["value"]
        duration = result["durationLabel"]["value"]
        review = result["reviewLabel"]["value"]
        icaa_rating = result["icaa_ratingLabel"]["value"]
        
        await fn_create_movie(imdb_id, title, icaa_rating, movies_repo)
        await fn_create_genre(imdb_id, genre, genres_repo)
        await fn_create_production(
            imdb_id, director, country, duration, producer, language, distributor, company, cost, date, productions_repo
        )
        await fn_create_review( imdb_id, review, reviews_repo )

    return StatusResponse(
        status = status.HTTP_201_CREATED,
        details = "Movies laoded from wikidata successfully"
    )
from app.models.domains.cast import NewCast
from app.models.domains.genre import NewGenre
from app.models.domains.movie import NewMovie
from app.models.domains.production import NewProduction
from app.models.domains.review import NewReview

def new_cast() -> NewCast:
    return NewCast(
        imdb_id='tt2980516',
        name='Emmanuel Okoro'
    )
    

def new_genre() -> NewGenre:
    return NewGenre(
        imdb_id='tt2980516',
        genre='Drama movie'
    )
    

def new_movie() -> NewMovie:
    return NewMovie(
        imdb_id='tt2980516',
        title='Black Panter',
        icaa_rating="18 years and above"
    )
    

def new_production() -> NewProduction:
    return NewProduction(
        imdb_id='tt2980516',
        director='Emmanuel Okoro',
        country='Nigeria',
        duration='120',
        producer='endiesworld',
        language='English',
        distributor='Emmys Enterprice',
        company='Appsilon',
        cost='1200000',
        date='May 30 2023'
    )
    
    
def new_review() -> NewReview:
    return NewReview(
        imdb_id='tt2980516',
        rating='9.5/10',
    )
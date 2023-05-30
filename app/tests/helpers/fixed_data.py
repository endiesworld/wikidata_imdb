from app.models.domains.cast import NewCast
from app.models.domains.genre import NewGenre

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
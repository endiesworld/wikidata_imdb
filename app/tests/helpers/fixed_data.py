from app.models.domains.cast import NewCast

def new_cast() -> NewCast:
    return NewCast(
        imdb_id='tt2980516',
        name='Emmanuel Okoro'
    )
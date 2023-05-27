from app.models.core import IDModelMixin, TimestampsMixin

class Genre(TimestampsMixin, IDModelMixin):
    imdb_id: str
    genre: str
    
    
class GenreDBModel(Genre):
    ...


NewGenre = Genre
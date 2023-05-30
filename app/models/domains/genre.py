from app.models.core import IDModelMixin, TimestampsMixin, CoreModel

class Genre(CoreModel):
    imdb_id: str
    genre: str
    
    
class GenreDBModel(Genre, TimestampsMixin):
    ...


NewGenre = Genre
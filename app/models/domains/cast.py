from app.models.core import IDModelMixin, TimestampsMixin

class Cast(TimestampsMixin, IDModelMixin):
    imdb_id: str
    name: str
    
    
class CastDBModel(Cast):
    ...


NewCast = Cast

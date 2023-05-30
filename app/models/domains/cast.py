from app.models.core import TimestampsMixin, CoreModel

class Cast(CoreModel):
    imdb_id: str
    name: str
    
    
class CastDBModel(Cast, TimestampsMixin):
    ...


NewCast = Cast

from pydantic import BaseModel

from app.models.entities import SimplestreamChannel


class SimplestreamSourceResponse(BaseModel):
    id: int
    index_url: str
    channel: SimplestreamChannel

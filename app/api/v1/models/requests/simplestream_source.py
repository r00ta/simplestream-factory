from pydantic import BaseModel

from app.models.entities import SimplestreamChannel


class SimplestreamSourceCreateRequest(BaseModel):
    index_url: str
    channel: SimplestreamChannel

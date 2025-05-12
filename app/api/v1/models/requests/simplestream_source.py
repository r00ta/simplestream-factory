from pydantic import BaseModel


class SimplestreamSourceCreateRequest(BaseModel):
    index_url: str

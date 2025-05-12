from typing import List

from pydantic import BaseModel

from app.models.entities import SimplestreamChannel, SimplestreamProductArch


class SimplestreamProductVersionResponse(BaseModel):
    id: int
    name: str
    channel: SimplestreamChannel

class SimplestreamProductResponse(BaseModel):
    id: int
    name: str
    arch: SimplestreamProductArch
    os: str
    versions: List[SimplestreamProductVersionResponse]

class SimplestreamProductsResponse(BaseModel):
    items: List[SimplestreamProductResponse]
    total: int

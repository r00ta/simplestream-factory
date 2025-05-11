from pydantic import BaseModel

from app.models.entities import SimplestreamProductArch, SimplestreamChannel


class SimplestreamsProductManifest(BaseModel):
    arch: SimplestreamProductArch
    os: str
    channel: SimplestreamChannel
    properties: dict
    versions: dict[str, dict]

class SimplestreamsSourceManifest(BaseModel):
    products: dict[str, SimplestreamsProductManifest]

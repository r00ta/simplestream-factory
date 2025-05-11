from pydantic import BaseModel

from app.models.entities import SimplestreamProductArch

class SimplestreamsProductManifest(BaseModel):
    arch: SimplestreamProductArch
    properties: dict
    versions: dict[str, dict]

class SimplestreamsSourceManifest(BaseModel):
    products: dict[str, SimplestreamsProductManifest]

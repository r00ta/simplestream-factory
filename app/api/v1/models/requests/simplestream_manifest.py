from pydantic import BaseModel

from app.models.entities import SimplestreamChannel


class ManifestSelectionRequest(BaseModel):
    version_ids: list[int]

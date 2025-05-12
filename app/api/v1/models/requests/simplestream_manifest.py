from pydantic import BaseModel


class ManifestSelectionRequest(BaseModel):
    version_ids: list[int]

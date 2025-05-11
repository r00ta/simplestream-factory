import uuid

from fastapi import Depends

from app.api.base import Handler, handler
from app.api.middlewares.services import services
from app.api.v1.models.requests.base import PaginationParams
from app.api.v1.models.requests.simplestream_manifest import ManifestSelectionRequest
from app.api.v1.models.requests.simplestream_source import SimplestreamSourceCreateRequest
from app.api.v1.models.responses.simplestream_source import SimplestreamSourceResponse
from app.services.collection import ServiceCollection


class SimplestreamManifestHandler(Handler):
    """Simplestream Manifest API handler."""

    @handler(path="/simplestreamsmanifests/{selector_id}/index.json", methods=["GET"])
    async def get_manifest_index(
        self,
        selector_id: str,
        services: ServiceCollection = Depends(services),
    ):
        return await services.simplestream_manifest.render_index(selector_id)

    @handler(path="/simplestreamsmanifests/{selector_id}/com.r00ta.spaghettihub:stable:chupa:download.json", methods=["GET"])
    async def get_manifest_product(
        self,
        selector_id: str,
        services: ServiceCollection = Depends(services),
    ):
        return await services.simplestream_manifest.render_product(selector_id)

    @handler(path="/simplestreamsmanifests", methods=["POST"])
    async def create_simplestreamsource(
        self,
        manifest_selection_request: ManifestSelectionRequest,
        services: ServiceCollection = Depends(services),
    ):
        selector_id = str(uuid.uuid4())
        simplestreamsource = await services.simplestream_manifest.create_selection(selector_id,
                                                                                   manifest_selection_request.version_ids)
        return {"selector_id": selector_id}
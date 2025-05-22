import os
import uuid

from fastapi import Depends
from starlette.requests import Request

from app.api.base import Handler, handler
from app.api.middlewares.services import services
from app.api.v1.models.requests.simplestream_manifest import ManifestSelectionRequest
from app.services.collection import ServiceCollection


class SimplestreamManifestHandler(Handler):
    """Simplestream Manifest API handler."""

    @handler(path="/simplestreamsmanifests/{selector_id}/streams/v1/index.json", methods=["GET"])
    async def get_manifest_index(
        self,
        selector_id: str,
        services: ServiceCollection = Depends(services),
    ):
        return await services.simplestream_manifest.render_index(selector_id)

    @handler(path="/simplestreamsmanifests/{selector_id}/streams/v1/com.r00ta.spaghettihub:stable:1:chupa:download.json",
             methods=["GET"])
    async def get_manifest_product(
        self,
        selector_id: str,
        services: ServiceCollection = Depends(services),
    ):
        return await services.simplestream_manifest.render_product(selector_id)

    @handler(path="/simplestreamsmanifests", methods=["POST"])
    async def create_simplestreamsource(
        self,
        request: Request,
        manifest_selection_request: ManifestSelectionRequest,
        services: ServiceCollection = Depends(services),
    ):
        selector_id = str(uuid.uuid4())
        await services.simplestream_manifest.create_selection(selector_id, manifest_selection_request.version_ids)
        base_url = str(request.base_url).rstrip("/")
        return {"simplestream_url": f"{base_url}/v1/simplestreamsmanifests/{selector_id}/streams/v1/index.json"}
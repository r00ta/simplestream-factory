import os
import uuid

from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse

from app.api.base import Handler, handler
from app.api.middlewares.services import services
from app.api.v1.models.requests.base import PaginationParams
from app.api.v1.models.requests.simplestream_manifest import ManifestSelectionRequest
from app.api.v1.models.requests.simplestream_source import SimplestreamSourceCreateRequest
from app.api.v1.models.responses.simplestream_source import SimplestreamSourceResponse
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
        simplestreamsource = await services.simplestream_manifest.create_selection(selector_id,
                                                                                   manifest_selection_request.version_ids)
        base_url = str(request.base_url).rstrip("/")
        return {"simplestream_url": f"{base_url}/v1/simplestreamsmanifests/{selector_id}/streams/v1/index.json"}

    @handler(path="/v1/simplestreamsmanifests/{selector_id}/{tail:path}", methods=["GET"])
    async def get_asset(self, selector_id: str, tail: str):
        sanitized_tail = os.path.normpath(tail).lstrip(os.sep)
        file_path = os.path.join("/tmp/images/", sanitized_tail)
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file_path)
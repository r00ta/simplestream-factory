from fastapi import Depends

from app.api.base import Handler, handler
from app.api.middlewares.services import services
from app.api.v1.models.requests.base import PaginationParams
from app.api.v1.models.requests.simplestream_source import SimplestreamSourceCreateRequest
from app.api.v1.models.responses.simplestream_source import SimplestreamSourceResponse
from app.services.collection import ServiceCollection


class SimplestreamSourceHandler(Handler):
    """Simplestream Source API handler."""

    @handler(path="/simplestreamsources", methods=["GET"])
    async def list_simplestreamsources(
        self,
        services: ServiceCollection = Depends(services),
        pagination_params: PaginationParams = Depends(),
    ):
        return await services.simplestream_source.list(
            page=pagination_params.page, size=pagination_params.size
        )

    @handler(path="/simplestreamsources", methods=["POST"])
    async def create_simplestreamsource(
        self,
        simplestreamsource_request: SimplestreamSourceCreateRequest,
        services: ServiceCollection = Depends(services),
    ):
        simplestreamsource = await services.simplestream_source.create(text=simplestreamsource_request.text)
        return SimplestreamSourceResponse(id=simplestreamsource.id, text=simplestreamsource.text)
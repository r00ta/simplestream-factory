from fastapi import Depends

from app.api.base import Handler, handler
from app.api.middlewares.services import services
from app.api.v1.models.requests.base import PaginationParams
from app.api.v1.models.requests.hello import HelloCreateRequest
from app.api.v1.models.responses.hello import HelloResponse
from app.services.collection import ServiceCollection


class HelloHandler(Handler):
    """Hello API handler."""

    @handler(path="/hello", methods=["GET"])
    async def list_hello(
        self,
        services: ServiceCollection = Depends(services),
        pagination_params: PaginationParams = Depends(),
    ):
        return await services.hello.list(
            page=pagination_params.page, size=pagination_params.size
        )

    @handler(path="/hello", methods=["POST"])
    async def create_hello(
        self,
        hello_request: HelloCreateRequest,
        services: ServiceCollection = Depends(services),
    ):
        hello = await services.hello.create(text=hello_request.text)
        return HelloResponse(id=hello.id, text=hello.text)
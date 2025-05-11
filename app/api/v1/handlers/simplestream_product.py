from fastapi import Depends

from app.api.base import Handler, handler
from app.api.middlewares.services import services
from app.api.v1.models.requests.base import PaginationParams
from app.api.v1.models.requests.simplestream_source import SimplestreamSourceCreateRequest
from app.api.v1.models.responses.simplestream_product import SimplestreamProductsResponse, SimplestreamProductResponse, \
    SimplestreamProductVersionResponse
from app.api.v1.models.responses.simplestream_source import SimplestreamSourceResponse
from app.services.collection import ServiceCollection


class SimplestreamProductHandler(Handler):
    """Simplestream Product API handler."""

    @handler(path="/simplestreamproducts", methods=["GET"])
    async def list_simplestreamproducts(
        self,
        services: ServiceCollection = Depends(services),
        pagination_params: PaginationParams = Depends(),
    ):
        products = await services.simplestream_product.list(
            page=pagination_params.page, size=pagination_params.size
        )

        return SimplestreamProductsResponse(
            items=[
                SimplestreamProductResponse(
                    id=product.id,
                    name=product.name,
                    arch=product.arch,
                    os=product.os,
                    versions=[
                        SimplestreamProductVersionResponse(
                            id=version.id,
                            name=version.name,
                            channel=version.channel
                        )
                        for version in product.versions
                    ]
                )
                for product in products.items
            ],
            total=products.total
        )

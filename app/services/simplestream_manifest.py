from datetime import datetime, timezone
from email.utils import format_datetime
from typing import List

from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.db.base import SessionProvider
from app.models.base import ListResult
from app.models.entities import SimplestreamProductVersion, ManifestSelection, \
    SimplestreamProduct
from app.services.base import BaseService
from app.services.simplestream_product import SimplestreamProductService
from app.services.simplestream_productversion import SimplestreamProductVersionService
from app.services.simplestream_source import SimplestreamSourceService


class SimplestreamManifetsService(BaseService[ManifestSelection]):
    def __init__(self,
                 session_provider: SessionProvider,
                 simplestream_source_service: SimplestreamSourceService,
                 simplestream_product_service: SimplestreamProductService,
                 simplestream_productversion_service: SimplestreamProductVersionService,
                 ):
        super().__init__(session_provider)
        self.simplestream_source_service = simplestream_source_service
        self.simplestream_product_service = simplestream_product_service
        self.simplestream_productversion_service = simplestream_productversion_service

    async def get(self, simplestreamsource_id: int) -> ManifestSelection | None:
        raise NotImplemented()

    async def list(self, page: int, size: int) -> ListResult[ManifestSelection]:
        raise NotImplemented()

    async def list_by_selector(self, selector_id: str) -> List[ManifestSelection]:
        stmt = select(ManifestSelection).where(ManifestSelection.selector_id == selector_id)
        result = await self.session.execute(stmt)
        selections = result.scalars().all()
        return selections

    async def delete(self, simplestreamsource_id: int) -> None:
        raise NotImplemented()

    async def create_selection(self, uuid: str, selections: List[int]):
        await self.session.execute(
            insert(ManifestSelection),
            [{"selector_id": uuid, "version_id": vid} for vid in selections]
        )

    async def _find_products(self, selector_id: str) -> List[SimplestreamProduct]:
        stmt = (
            select(SimplestreamProduct)
            .options(selectinload(SimplestreamProduct.versions))
            .join(SimplestreamProduct.versions)
            .join(ManifestSelection, ManifestSelection.version_id == SimplestreamProductVersion.id)
            .where(ManifestSelection.selector_id == selector_id)
            .distinct()
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


    async def render_index(self, selector_id: str) -> dict:
        products = await self._find_products(selector_id)
        return {
            "format": "index:1.0",
            "updated": format_datetime(datetime.now(timezone.utc)),
            "index": {
                "com.r00ta.spaghettihub:stable:chupa:download.json": {
                    "datatype": "image-ids",
                    "format": "products:1.0",
                    "path": "streams/v1/com.r00ta.spaghettihub:stable:1:chupa:download.json",
                    "updated": format_datetime(datetime.now(timezone.utc)),
                    "products": [product.name for product in products]
                }
            }
        }

    def _update_paths(self, data, channel):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "path" and isinstance(value, str):
                    data[key] = f"{channel}/{value}"
                else:
                    self._update_paths(value, channel)
        elif isinstance(data, list):
            for item in data:
                self._update_paths(item, channel)
        return data

    async def render_product(self, selector_id: str) -> dict:
        selections = await self.list_by_selector(selector_id)
        selections_ids = {selection.version_id for selection in selections}
        products = await self._find_products(selector_id)
        products_response = {}
        for product in products:
            tmpproduct = product.properties
            versions = {}
            for version in product.versions:
                if version.id not in selections_ids:
                    continue
                version.properties = self._update_paths(version.properties, version.channel.value.lower())
                versions[version.name] = version.properties
            tmpproduct["versions"] = versions
            products_response.update({product.name: tmpproduct})

        response = {}
        response["content_id"] = "com.r00ta.spaghettihub:stable:1:chupa:download.json"
        response["datatype"] = "image-ids"
        response["format"] = "products:1.0"
        response["updated"] = format_datetime(datetime.now(timezone.utc))
        response["products"] = products_response
        return response


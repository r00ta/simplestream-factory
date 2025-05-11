from typing import List

from sqlalchemy import func, select

from app.db.base import SessionProvider
from app.models.base import ListResult
from app.models.entities import SimplestreamChannel, SimplestreamProductVersion, SimplestreamSource, SimplestreamProduct
from app.services.base import BaseService, Query


class SimplestreamProductVersionService(BaseService[SimplestreamProductVersion]):
    def __init__(self, session_provider: SessionProvider):
        super().__init__(session_provider)

    async def get(self, simplestreamproduct_id: int) -> SimplestreamProductVersion | None:
        stmt = select(SimplestreamProductVersion).filter(SimplestreamProductVersion.id == simplestreamproduct_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_name(self, simplestreamproduct_id: int, simplestreamproduct_name: str) -> SimplestreamProductVersion | None:
        stmt = (
            select(SimplestreamProductVersion)
            .where(
                SimplestreamProductVersion.name == simplestreamproduct_name,
                SimplestreamProductVersion.product_id == simplestreamproduct_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self, page: int, size: int) -> ListResult[SimplestreamProductVersion]:
        stmt = select(SimplestreamProductVersion).limit(size).offset((page - 1) * size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count()).select_from(SimplestreamProductVersion)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return ListResult[SimplestreamProductVersion](items=items, total=total)

    async def list_with_query(self, query: Query) -> List[SimplestreamProductVersion]:
        stmt = select(SimplestreamProductVersion)

        if query.filters is not None:
            for condition in query.filters:
                stmt = stmt.where(condition)

        if query.sort is not None:
            for sort_criterion in query.sort:
                stmt = stmt.order_by(sort_criterion)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, simplestreamproductversion_id: int) -> None:
        stmt = select(SimplestreamProductVersion).filter(SimplestreamProductVersion.id == simplestreamproductversion_id)
        result = await self.session.execute(stmt)
        simplestreamproductversion = result.scalars().first()
        if simplestreamproductversion:
            await self.session.delete(simplestreamproductversion)

    async def create(self,
                     name: str,
                     properties: dict,
                     product: SimplestreamProduct,
                     channel: SimplestreamChannel
                     ) -> SimplestreamProductVersion:
        simplestreamproductversion = SimplestreamProductVersion(
            name=name,
            properties=properties,
            product=product,
            channel=channel
        )
        self.session.add(simplestreamproductversion)
        return simplestreamproductversion
from sqlalchemy import func, select

from app.db.base import SessionProvider
from app.models.base import ListResult
from app.models.entities import SimplestreamChannel, SimplestreamProduct, SimplestreamProductArch, SimplestreamSource
from app.services.base import BaseService


class SimplestreamProductService(BaseService[SimplestreamProduct]):
    def __init__(self, session_provider: SessionProvider):
        super().__init__(session_provider)

    async def get(self, simplestreamproduct_id: int) -> SimplestreamProduct | None:
        stmt = select(SimplestreamProduct).filter(SimplestreamProduct.id == simplestreamproduct_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_name(self, simplestreamsource_id: int, simplestreamproduct_name: str) -> SimplestreamProduct | None:
        stmt = (
            select(SimplestreamProduct)
            .where(
                SimplestreamProduct.name == simplestreamproduct_name,
                SimplestreamProduct.source_id == simplestreamsource_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self, page: int, size: int) -> ListResult[SimplestreamProduct]:
        stmt = select(SimplestreamProduct).limit(size).offset((page - 1) * size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count()).select_from(SimplestreamProduct)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return ListResult[SimplestreamProduct](items=items, total=total)

    async def delete(self, simplestreamproduct_id: int) -> None:
        stmt = select(SimplestreamProduct).filter(SimplestreamProduct.id == simplestreamproduct_id)
        result = await self.session.execute(stmt)
        simplestreamproduct = result.scalars().first()
        if simplestreamproduct:
            await self.session.delete(simplestreamproduct)

    async def create(self,
                     name: str,
                     arch: SimplestreamProductArch,
                     properties: dict,
                     source: SimplestreamSource,
                     ) -> SimplestreamProduct:
        simplestreamproduct = SimplestreamProduct(
            name=name,
            arch=arch,
            properties=properties,
            source=source
        )
        self.session.add(simplestreamproduct)
        return simplestreamproduct
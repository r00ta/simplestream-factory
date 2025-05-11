from sqlalchemy import func, select

from app.db.base import SessionProvider
from app.models.base import ListResult
from app.models.entities import SimplestreamSource, SimplestreamChannel
from app.services.base import BaseService


class SimplestreamSourceService(BaseService[SimplestreamSource]):
    def __init__(self, session_provider: SessionProvider):
        super().__init__(session_provider)

    async def get(self, simplestreamsource_id: int) -> SimplestreamSource | None:
        stmt = select(SimplestreamSource).filter(SimplestreamSource.id == simplestreamsource_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self, page: int, size: int) -> ListResult[SimplestreamSource]:
        stmt = select(SimplestreamSource).limit(size).offset((page - 1) * size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count()).select_from(SimplestreamSource)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return ListResult[SimplestreamSource](items=items, total=total)

    async def delete(self, simplestreamsource_id: int) -> None:
        stmt = select(SimplestreamSource).filter(SimplestreamSource.id == simplestreamsource_id)
        result = await self.session.execute(stmt)
        simplestreamsource = result.scalars().first()
        if simplestreamsource:
            await self.session.delete(simplestreamsource)

    async def create(self, index_url: str, channel: SimplestreamChannel) -> SimplestreamSource:
        simplestreamsource = SimplestreamSource(index_url=index_url, channel=channel)
        self.session.add(simplestreamsource)
        return simplestreamsource
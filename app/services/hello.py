from sqlalchemy import func, select

from app.db.base import SessionProvider
from app.models.base import ListResult
from app.models.entities import Hello
from app.services.base import BaseService


class HelloService(BaseService[Hello]):
    def __init__(self, session_provider: SessionProvider):
        super().__init__(session_provider)

    async def get(self, hello_id: int) -> Hello | None:
        stmt = select(Hello).filter(Hello.id == hello_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self, page: int, size: int) -> ListResult[Hello]:
        stmt = select(Hello).limit(size).offset((page - 1) * size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        count_stmt = select(func.count()).select_from(Hello)
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar_one()

        return ListResult(items=items, total=total)

    async def delete(self, hello_id: int) -> None:
        stmt = select(Hello).filter(Hello.id == hello_id)
        result = await self.session.execute(stmt)
        hello = result.scalars().first()
        if hello:
            await self.session.delete(hello)

    async def create(self, text: str) -> Hello:
        hello = Hello(text=text)
        self.session.add(hello)
        return hello

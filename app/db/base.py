from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session


@dataclass
class SessionProvider:
    current_session: Session | None

    def get_current_session(self) -> Session:
        return self.current_session


class DatabaseConfig(ABC):
    @abstractmethod
    def get_dsn(self) -> URL:
        pass

    @abstractmethod
    def get_isolation_level(self) -> str:
        pass


@dataclass
class PostgresDatabaseConfig(DatabaseConfig):
    name: str
    host: str
    username: str | None = None
    password: str | None = None
    port: int | None = None

    def get_dsn(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            host=self.host,
            port=self.port,
            database=self.name,
            username=self.username,
            password=self.password,
        )

    def get_isolation_level(self) -> str:
        return "REPEATABLE READ"


@dataclass
class SQLiteDatabaseConfig(DatabaseConfig):
    path: str = "db.sqlite"

    def get_dsn(self) -> URL:
        return URL.create(
            "sqlite+aiosqlite",
            database=self.path,
        )

    def get_isolation_level(self) -> str:
        return "SERIALIZABLE"


class Database:
    def __init__(self, config: DatabaseConfig, echo: bool = False):
        self.config = config
        self.engine = create_async_engine(
            config.get_dsn(), echo=echo, isolation_level=config.get_isolation_level()
        )
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    @asynccontextmanager
    async def begin_session(self):
        async with self.sessionmaker() as session:
            async with session.begin():
                yield session

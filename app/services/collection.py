from dataclasses import dataclass

from app.db.base import SessionProvider
from app.services.hello import HelloService


@dataclass
class ServiceCollection:
    hello: HelloService

    @classmethod
    def produce(cls, session_provider: SessionProvider) -> "ServiceCollection":
        return cls(hello=HelloService(session_provider))

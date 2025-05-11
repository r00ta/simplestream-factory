from dataclasses import dataclass

from app.db.base import SessionProvider
from app.services.simplestream_manifest import SimplestreamManifetsService
from app.services.simplestream_product import SimplestreamProductService
from app.services.simplestream_productversion import SimplestreamProductVersionService
from app.services.simplestream_source import SimplestreamSourceService


@dataclass
class ServiceCollection:
    simplestream_source: SimplestreamSourceService
    simplestream_product: SimplestreamProductService
    simplestream_productversion: SimplestreamProductVersionService
    simplestream_manifest: SimplestreamManifetsService

    @classmethod
    def produce(cls, session_provider: SessionProvider) -> "ServiceCollection":
        simplestream_source = SimplestreamSourceService(session_provider)
        simplestream_product = SimplestreamProductService(session_provider)
        simplestream_productversion = SimplestreamProductVersionService(session_provider)
        return cls(
            simplestream_source=simplestream_source,
            simplestream_product=simplestream_product,
            simplestream_productversion = simplestream_productversion,
            simplestream_manifest = SimplestreamManifetsService(
                session_provider,
                simplestream_source,
                simplestream_product,
                simplestream_productversion
            )
        )

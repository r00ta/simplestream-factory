import logging
import os

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.middlewares.db import TransactionMiddleware
from app.api.middlewares.services import ServicesMiddleware
from app.api.static import APIstatic
from app.api.v1 import APIv1
from app.db.base import Database, SessionProvider
from app.services.collection import ServiceCollection
from app.settings import Settings
from app.simplestream.parser import SimplestreamParser

logger = logging.getLogger()

app = FastAPI()

settings = Settings()
db = Database(settings.get_db_config(), echo=False)

app.add_middleware(ServicesMiddleware)
app.add_middleware(TransactionMiddleware, db=db)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=os.path.join(os.getcwd(), "dist", "assets")), name="static")
APIstatic.register(app.router)
APIv1.register(app.router)

@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
async def remove_expired_tokens_task() -> None:
    try:
        async with db.begin_session() as session:
            session_provider = SessionProvider(current_session=session)
            services = ServiceCollection.produce(session_provider)
            parser = SimplestreamParser()
            sources = await services.simplestream_source.list(1, 1000)
            for source in sources.items:
                manifest = await parser.download(source.index_url)
                for product_name, manifest_product in manifest.products.items():
                    product = await services.simplestream_product.get_by_name(product_name)
                    if product is None:
                        product = await services.simplestream_product.create(
                            name=product_name,
                            arch=manifest_product.arch,
                            os=manifest_product.os,
                            properties=manifest_product.properties,
                        )
                        logger.info(f"Product {product.name} has been created")
                    for version_name, manifest_version in manifest_product.versions.items():
                        productversion = await services.simplestream_productversion.get_by_name(product.id, version_name)
                        if productversion is None:
                            productversion = await services.simplestream_productversion.create(
                                name=version_name,
                                properties=manifest_version,
                                product=product,
                                channel=manifest_product.channel
                            )
                            logger.info(f"Version {productversion.name} for product {product.name} has been created")
    except Exception as e:
        print(e)
from app.api.base import API
from app.api.v1.handlers.root import RootHandler
from app.api.v1.handlers.simplestream_manifest import SimplestreamManifestHandler
from app.api.v1.handlers.simplestream_product import SimplestreamProductHandler

APIv1 = API(
    prefix="/v1",
    handlers=[
        RootHandler(),
        SimplestreamProductHandler(),
        SimplestreamManifestHandler()
    ],
)

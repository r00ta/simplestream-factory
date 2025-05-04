from app.api.base import API
from app.api.v1.handlers.hello import HelloHandler
from app.api.v1.handlers.root import RootHandler

APIv1 = API(
    prefix="/v1",
    handlers=[
        RootHandler(),
        HelloHandler()
    ],
)

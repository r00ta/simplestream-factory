from app.api.base import API
from app.api.static.root import RootHandler

APIstatic = API(
    prefix="",
    handlers=[
        RootHandler(),
    ],
)

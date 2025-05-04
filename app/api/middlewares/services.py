from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.db.base import SessionProvider
from app.services.collection import ServiceCollection


def services(request: Request) -> ServiceCollection:
    return request.state.services


class ServicesMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        session_provider = SessionProvider(current_session=request.state.session)
        request.state.services = ServiceCollection.produce(session_provider)
        return await call_next(request)

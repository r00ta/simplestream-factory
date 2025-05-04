import logging
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.db.base import Database

logger = logging.getLogger()


class TransactionMiddleware(BaseHTTPMiddleware):
    """Run a request in a transaction, handling commit/rollback.

    This makes the database connection available as `request.state.conn`.
    """

    def __init__(self, app: ASGIApp, db: Database):
        super().__init__(app)
        self.db = db

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        async with self.db.begin_session() as session:
            request.state.session = session
            response = await call_next(request)
        return response

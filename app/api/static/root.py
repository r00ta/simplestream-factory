import os

from starlette.responses import HTMLResponse

from app.api.base import Handler, handler


class RootHandler(Handler):
    """Root API handler."""

    @handler(path="/", methods=["GET"], include_in_schema=False)
    async def serve_index(self):
        with open(os.path.join(os.getcwd(), "dist", "index.html")) as f:
            return HTMLResponse(content=f.read())

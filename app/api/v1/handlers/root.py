from app.api.base import Handler, handler


class RootHandler(Handler):
    """Root API handler."""

    @handler(path="/", methods=["GET"], include_in_schema=False)
    async def get(self):
        return {}

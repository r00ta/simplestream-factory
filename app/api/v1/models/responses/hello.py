from pydantic import BaseModel


class HelloResponse(BaseModel):
    id: int
    text: str
from pydantic import BaseModel


class HelloCreateRequest(BaseModel):
    text: str

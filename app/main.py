from fastapi import FastAPI

from app.api.middlewares.db import TransactionMiddleware
from app.api.middlewares.services import ServicesMiddleware
from app.api.v1 import APIv1
from app.db.base import Database
from app.settings import Settings

app = FastAPI()

settings = Settings()
db = Database(settings.get_db_config(), echo=False)

app.add_middleware(ServicesMiddleware)
app.add_middleware(TransactionMiddleware, db=db)
APIv1.register(app.router)

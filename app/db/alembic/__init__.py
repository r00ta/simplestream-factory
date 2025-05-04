from importlib.resources import files

from alembic.config import Config

from app.settings import Settings


def get_config() -> Config:
    file_name = str(files("app.db.alembic") / "alembic.ini")
    config = Config(file_name)
    settings = Settings()
    config.set_main_option(
        "sqlalchemy.url",
        settings.get_db_config().get_dsn().render_as_string(
            hide_password=False
        ),
    )
    return config

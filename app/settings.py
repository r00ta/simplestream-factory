from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.db.base import DatabaseConfig, PostgresDatabaseConfig, SQLiteDatabaseConfig


class Settings(BaseSettings):

    model_config = SettingsConfigDict(case_sensitive=True)

    db: str = Field(default="postgres", validate_alias="APP_DB")
    postgres_db_host: str = Field(
        default="localhost",
        validation_alias="APP_DB_HOST",
    )
    postgres_db_port: int = Field(
        default=5432,
        validation_alias="APP_DB_PORT",
    )
    postgres_db_name: str | None = Field(
        default="app",
        validation_alias="APP_DB_NAME",
    )
    postgres_db_user: str | None = Field(
        default="app",
        validation_alias="APP_DB_USER",
    )
    postgres_db_password: SecretStr | None = Field(
        default="app",
        validation_alias="APP_DB_PASSWORD",
    )
    sqlite_db_path: str | None = Field(
        default="db.sqlite",
        validation_alias="SQLITE_DB_PATH",
    )

    def get_db_config(self) -> DatabaseConfig:
        """The DSN, from configured settings."""
        if self.db == "postgres":
            return SQLiteDatabaseConfig(path=self.sqlite_db_path)
        else:
            return PostgresDatabaseConfig(
                host=self.postgres_db_host,
                port=self.postgres_db_port,
                name=self.postgres_db_name,
                username=self.postgres_db_user,
                password=self.postgres_db_password.get_secret_value()
                if self.db_password
                else None,
            )

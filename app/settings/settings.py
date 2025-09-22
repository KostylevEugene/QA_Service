from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


class AppSettings(GeneralSettings):
    app_workers: int = Field(default=1, validation_alias="APP_WORKERS")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    app_port: int = Field(default=7001, validation_alias="APP_PORT")
    log_size: str = Field(default="10 MB", validation_alias="LOG_SIZE")


class PGDBSettings(GeneralSettings):
    user: str = Field(
        default="postgres_user", validation_alias="POSTGRES_USER"
    )
    password: str = Field(
        default="postgres_password", validation_alias="POSTGRES_PASSWORD"
    )
    db_name: str = Field(default="postgres", validation_alias="POSTGRES_DB")
    host: str = Field(default="postgres", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")


app_settings = AppSettings()
postgres_db_settings = PGDBSettings()

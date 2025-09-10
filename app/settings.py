from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class SrvSettings(BaseSettings):
    app_name: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SRV_")


class LoggingConfig(BaseSettings):
    level: str
    json_enabled: bool
    extra_context: bool
    ignore_paths: list[str]
    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOGGING_")


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    database: str
    echo: bool

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.database,
            )
        )

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")


class HttpClientSettings(BaseSettings):
    base_url: str
    timeout: int
    verify_ssl: bool


class OpenAISettings(HttpClientSettings):
    proxy: str | None = None
    api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="OPENAI_")


class Settings(BaseSettings):
    load_dotenv()
    srv: SrvSettings = SrvSettings()
    logging: LoggingConfig = LoggingConfig()
    database: DatabaseSettings = DatabaseSettings()
    openai: OpenAISettings = OpenAISettings()

settings = Settings()

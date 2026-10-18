from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Aegis 2.0 API"
    environment: str = "development"
    api_prefix: str = "/api"
    cors_origins: str = "http://localhost:5173"
    database_url: str = "postgresql+psycopg://aegis:aegis_dev_only@localhost:5432/aegis"
    google_safe_browsing_api_key: str = ""
    virustotal_api_key: str = ""
    model_path: str = "../ml_engine/models/phishing_model.joblib"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

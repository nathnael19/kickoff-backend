from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    DB_SERVER: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    NEON_URL: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
        validate_default=False,
    )

    @property
    def postgres_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def online_url(self):
        return self.NEON_URL


settings = DBSettings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration class for the Financial Research Agent.
    All environment variables are loaded from the .env file.
    """

    APP_NAME: str = "Financial Research Agent"
    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    DEFAULT_MODEL: str = "gemini-2.5-flash"

    TEMPERATURE: float = 0.2

    MAX_RETRIES: int = 3

    TIMEOUT: int = 60

    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
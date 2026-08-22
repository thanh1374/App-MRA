"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configuration loaded from .env file or environment."""

    # API Keys
    appstorespy_api_key: str = Field(default="", description="AppstoreSpy API key")
    gemini_api_key: str = Field(default="", description="Gemini API key")

    # AppstoreSpy
    appstorespy_base_url: str = Field(
        default="https://api.appstorespy.com/v1",
        description="AppstoreSpy API base URL",
    )

    # Defaults
    default_store: str = Field(default="google_play", description="Default store")
    default_country: str = Field(default="US", description="Default country")
    default_language: str = Field(default="en_US", description="Default language")

    # Limits
    top_apps_limit: int = Field(default=5, description="Number of top apps to fetch")
    request_timeout: int = Field(default=30, description="HTTP request timeout (s)")
    gemini_max_retries: int = Field(
        default=2, description="Max retries for invalid Gemini JSON"
    )

    # CORS
    frontend_origin: str = Field(
        default="http://localhost:5173", description="Frontend origin for CORS"
    )

    # Paths
    template_path: str = Field(
        default="templates/Template.xlsx",
        description="Path to Excel template",
    )
    output_dir: str = Field(default="output", description="Output directory")
    cache_dir: str = Field(default="cache", description="Cache directory")
    log_dir: str = Field(default="logs", description="Log directory")

    # Cache
    cache_ttl_seconds: int = Field(
        default=3600, description="Cache TTL in seconds (1 hour)"
    )

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

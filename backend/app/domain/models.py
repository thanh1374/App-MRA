"""Domain models — internal normalized schemas."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StoreType(str, Enum):
    """Supported app stores."""

    GOOGLE_PLAY = "google_play"
    APP_STORE = "app_store"


class SourceType(str, Enum):
    """Data source tag for traceability."""

    API_FACT = "API_FACT"
    GEMINI_INFERENCE = "GEMINI_INFERENCE"
    GEMINI_RECOMMENDATION = "GEMINI_RECOMMENDATION"


class SourceTaggedValue(BaseModel):
    """A value paired with its data source."""

    value: object
    source: SourceType


class NormalizedApp(BaseModel):
    """Internal normalized app schema.

    Adapter maps real AppstoreSpy fields into this model.
    Missing fields are null — never guessed.
    """

    rank: int = Field(description="Position in search results (1-based)")
    app_id: str = Field(description="App package name / bundle ID")
    name: str = Field(description="App name")
    developer_name: Optional[str] = None
    category: Optional[str] = None
    description_short: Optional[str] = None
    description_full: Optional[str] = None
    rating: Optional[float] = Field(None, description="Rating value")
    rating_count: Optional[int] = None
    review_count: Optional[int] = None
    downloads: Optional[int] = Field(None, description="Exact installs or estimated")
    downloads_month: Optional[int] = None
    downloads_lifetime: Optional[int] = None
    revenue: Optional[int] = None
    revenue_month: Optional[int] = None
    revenue_lifetime: Optional[int] = None
    iap: Optional[bool] = Field(None, description="Has in-app purchases")
    update_date: Optional[str] = None
    release_date: Optional[str] = None
    version: Optional[str] = None
    icon: Optional[str] = None
    available_languages: Optional[list[str]] = None
    top_countries_downloads: Optional[list[str]] = None
    top_countries_revenue: Optional[list[str]] = None
    country: str = "US"
    language: str = "en_US"
    store: StoreType = StoreType.GOOGLE_PLAY


class AnalysisJob(BaseModel):
    """An analysis job result stored in memory."""

    job_id: str
    keyword: str
    store: StoreType
    country: str
    language: str
    apps: list[NormalizedApp] = []
    analysis: Optional[dict] = None
    status: str = "pending"  # pending | searching | analyzing | completed | error
    error: Optional[str] = None

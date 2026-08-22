"""API request/response schemas (FastAPI-facing)."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request body for POST /api/analyze."""

    keyword: str = Field(min_length=1, description="Search keyword")
    store: str = Field(default="google_play", description="google_play or app_store")
    country: str = Field(default="US", description="Country code")
    language: str = Field(default="en_US", description="Language code")
    appstorespy_api_key: Optional[str] = Field(
        None, description="AppstoreSpy API key (override .env)"
    )
    gemini_api_key: Optional[str] = Field(
        None, description="Gemini API key (override .env)"
    )


class AppSummary(BaseModel):
    """Compact app info for frontend display."""

    rank: int
    app_id: str
    name: str
    developer_name: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = None
    downloads: Optional[int] = None
    icon: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """Response body for POST /api/analyze."""

    job_id: str
    keyword: str
    store: str
    country: str
    apps: list[AppSummary] = []
    analysis: Optional[dict] = None
    status: str = "completed"
    error: Optional[str] = None


class ExportRequest(BaseModel):
    """Request body for POST /api/export."""

    job_id: str


class ErrorResponse(BaseModel):
    """Standardized error response."""

    error_code: str
    message: str
    detail: Optional[str] = None

"""Analyze endpoint — runs the full analysis pipeline."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.api.schemas import AnalyzeRequest, AnalyzeResponse, AppSummary
from app.application.analyze_service import run_analysis
from app.infrastructure.appstorespy_client import AppstoreSpyError
from app.infrastructure.gemini_client import GeminiError

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Run market research analysis for a keyword.

    Flow: validate → AppstoreSpy → normalize → Gemini → Pydantic → return
    """
    try:
        job = await run_analysis(
            keyword=request.keyword,
            store=request.store,
            country=request.country,
            language=request.language,
            appstorespy_api_key=request.appstorespy_api_key,
            gemini_api_key=request.gemini_api_key,
        )

        # Build app summaries for frontend
        app_summaries = [
            AppSummary(
                rank=app.rank,
                app_id=app.app_id,
                name=app.name,
                developer_name=app.developer_name,
                category=app.category,
                rating=app.rating,
                rating_count=app.rating_count,
                downloads=app.downloads,
                icon=app.icon,
            )
            for app in job.apps
        ]

        return AnalyzeResponse(
            job_id=job.job_id,
            keyword=job.keyword,
            store=job.store.value,
            country=job.country,
            apps=app_summaries,
            analysis=job.analysis,
            status=job.status,
        )

    except AppstoreSpyError as exc:
        logger.error("AppstoreSpy error: %s (status=%s)", exc.message, exc.status_code)
        error_code = {
            403: "INVALID_API_KEY",
            429: "RATE_LIMIT",
            202: "APP_CRAWLING",
            204: "NO_DATA",
        }.get(exc.status_code or 0, "APPSTORESPY_ERROR")
        raise HTTPException(
            status_code=400 if exc.status_code in (202, 204) else (exc.status_code or 500),
            detail={
                "error_code": error_code,
                "message": exc.message,
            },
        )

    except GeminiError as exc:
        logger.error("Gemini error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail={
                "error_code": "GEMINI_ERROR",
                "message": str(exc),
            },
        )

    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "VALIDATION_ERROR",
                "message": str(exc),
            },
        )

    except Exception as exc:
        logger.exception("Unexpected error during analysis")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "Lỗi không mong đợi. Vui lòng thử lại.",
            },
        )

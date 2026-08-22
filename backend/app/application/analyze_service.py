"""Analyze service — orchestrates the full analysis pipeline."""

from __future__ import annotations

import logging
import uuid
from pathlib import Path

from app.config.settings import settings
from app.domain.models import AnalysisJob, NormalizedApp, StoreType
from app.domain.schemas import GeminiAnalysisResult
from app.infrastructure.appstorespy_client import AppstoreSpyClient
from app.infrastructure.gemini_client import GeminiClient

logger = logging.getLogger(__name__)

# In-memory job storage (Phase 1 — no database)
_jobs: dict[str, AnalysisJob] = {}


def get_job(job_id: str) -> AnalysisJob | None:
    """Retrieve a stored analysis job."""
    return _jobs.get(job_id)


async def run_analysis(
    keyword: str,
    store: str = "google_play",
    country: str = "US",
    language: str = "en_US",
    appstorespy_api_key: str | None = None,
    gemini_api_key: str | None = None,
) -> AnalysisJob:
    """Execute the full analysis pipeline.

    Flow:
      1. AppstoreSpy search → TOP 5
      2. Normalize data
      3. Gemini analysis
      4. Pydantic validation
      5. Store result and return
    """
    job_id = str(uuid.uuid4())[:8]
    store_type = StoreType(store)

    job = AnalysisJob(
        job_id=job_id,
        keyword=keyword,
        store=store_type,
        country=country,
        language=language,
        status="searching",
    )
    _jobs[job_id] = job

    try:
        # Resolve API keys: request override > .env
        spy_key = appstorespy_api_key or settings.appstorespy_api_key
        gem_key = gemini_api_key or settings.gemini_api_key

        if not spy_key:
            raise ValueError("AppstoreSpy API key không được cung cấp.")
        if not gem_key:
            raise ValueError("Gemini API key không được cung cấp.")

        # Step 1: Search AppstoreSpy
        logger.info("Step 1: Searching AppstoreSpy for '%s'", keyword)
        spy_client = AppstoreSpyClient(
            api_key=spy_key,
            base_url=settings.appstorespy_base_url,
            timeout=settings.request_timeout,
        )
        apps = await spy_client.search_apps(
            keyword=keyword,
            store=store_type,
            country=country,
            language=language,
            limit=settings.top_apps_limit,
        )

        if not apps:
            raise ValueError(f"Không tìm thấy app nào cho keyword '{keyword}'.")

        job.apps = apps
        job.status = "enriching"
        logger.info("Step 1 done: found %d apps", len(apps))

        # Step 1.5: Enrich with detail API (languages, top countries)
        logger.info("Step 1.5: Enriching apps with detail data")
        apps = await spy_client.enrich_apps(
            apps=apps,
            store=store_type,
            country=country,
            language=language,
        )
        job.apps = apps
        job.status = "analyzing"
        logger.info("Step 1.5 done: apps enriched with geo/language data")

        # Step 2: Gemini analysis
        logger.info("Step 2: Sending data to Gemini")
        gemini = GeminiClient(
            api_key=gem_key,
            max_retries=settings.gemini_max_retries,
        )
        analysis: GeminiAnalysisResult = await gemini.analyze(
            keyword=keyword,
            store=store,
            country=country,
            apps=apps,
        )

        job.analysis = analysis.model_dump()
        job.status = "completed"
        logger.info("Step 2 done: Gemini analysis completed")

    except Exception as exc:
        logger.error("Analysis failed: %s", exc)
        job.status = "error"
        job.error = str(exc)
        raise

    return job

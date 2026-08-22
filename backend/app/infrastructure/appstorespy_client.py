"""AppstoreSpy REST API client.

Maps real OpenAPI schema fields (PlayApp / IosApp) into NormalizedApp.
Never assumes a field exists — only uses fields confirmed in the OpenAPI spec.
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.domain.models import NormalizedApp, StoreType

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PlayApp fields (from OpenAPI schema) → NormalizedApp mapping
# ---------------------------------------------------------------------------
# PlayApp uses: name, short (→ description_short), description (→ description_full),
# developer_name, category, rating_value (→ rating), rating_count,
# review_count, installs_exact (→ downloads), revenue, iap,
# updated (→ update_date), released (→ release_date), version, icon,
# downloads (estimated monthly), id (→ app_id)
# ---------------------------------------------------------------------------


class AppstoreSpyError(Exception):
    """Base error for AppstoreSpy client."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AppstoreSpyClient:
    """Async HTTP client for AppstoreSpy v1 API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.appstorespy.com/v1",
        timeout: int = 30,
    ):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "API-KEY": self._api_key,
            "Accept": "application/json",
        }

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    async def search_apps(
        self,
        keyword: str,
        store: StoreType = StoreType.GOOGLE_PLAY,
        country: str = "US",
        language: str = "en_US",
        limit: int = 5,
    ) -> list[NormalizedApp]:
        """Search for apps and return normalized results.

        TOP N apps = first N items returned by AppstoreSpy.
        No custom sort is applied (spec requirement).
        """
        if store == StoreType.GOOGLE_PLAY:
            endpoint = f"{self._base_url}/play/apps"
            params: dict = {
                "q": keyword,
                "country": country,
                "language": language,
                "limit": limit,
                "page": 1,
                "sort": "-downloads",
            }
        else:
            endpoint = f"{self._base_url}/ios/apps"
            params = {
                "q": keyword,
                "country": country,
                "limit": limit,
                "page": 1,
                "sort": "-downloads",
            }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            logger.info(
                "AppstoreSpy search: %s store=%s country=%s keyword=%r",
                endpoint,
                store.value,
                country,
                keyword,
            )
            response = await client.get(
                endpoint, params=params, headers=self._headers()
            )

        self._handle_status(response)

        data = response.json()
        if not isinstance(data, list):
            data = data.get("data", []) if isinstance(data, dict) else []

        apps: list[NormalizedApp] = []
        for idx, item in enumerate(data[:limit], start=1):
            app = self._normalize(item, idx, store, country, language)
            apps.append(app)

        logger.info("AppstoreSpy returned %d apps for %r", len(apps), keyword)
        return apps

    # ------------------------------------------------------------------
    # Detail (optional — only if search response is insufficient)
    # ------------------------------------------------------------------

    async def get_app_detail(
        self,
        app_id: str,
        store: StoreType = StoreType.GOOGLE_PLAY,
        country: str = "US",
        language: str = "en_US",
    ) -> dict:
        """Fetch detailed app data by ID."""
        if store == StoreType.GOOGLE_PLAY:
            endpoint = f"{self._base_url}/play/apps/{app_id}"
        else:
            endpoint = f"{self._base_url}/ios/apps/{app_id}"

        params: dict = {"country": country, "language": language}

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                endpoint, params=params, headers=self._headers()
            )

        self._handle_status(response)
        return response.json()

    # ------------------------------------------------------------------
    # Enrich — call detail API to fill missing geo/language fields
    # ------------------------------------------------------------------

    async def enrich_apps(
        self,
        apps: list[NormalizedApp],
        store: StoreType = StoreType.GOOGLE_PLAY,
        country: str = "US",
        language: str = "en_US",
    ) -> list[NormalizedApp]:
        """Enrich apps with detail data (languages, top countries).

        The search endpoint often omits languages, top_countries_downloads,
        and top_countries_revenue. This calls the detail endpoint for each
        app to fill those fields in.
        """
        enriched: list[NormalizedApp] = []

        for app in apps:
            needs_enrich = (
                not app.available_languages
                or not app.top_countries_downloads
                or not app.top_countries_revenue
            )

            if not needs_enrich:
                enriched.append(app)
                continue

            try:
                logger.info(
                    "Enriching app detail: %s (%s)", app.name, app.app_id
                )
                detail = await self.get_app_detail(
                    app_id=app.app_id,
                    store=store,
                    country=country,
                    language=language,
                )

                # Fill missing fields from detail response
                if not app.available_languages and detail.get("languages"):
                    app.available_languages = detail["languages"]

                if not app.top_countries_downloads and detail.get("top_countries_downloads"):
                    app.top_countries_downloads = detail["top_countries_downloads"]

                if not app.top_countries_revenue and detail.get("top_countries_revenue"):
                    app.top_countries_revenue = detail["top_countries_revenue"]

                # Also enrich other potentially missing fields
                if not app.description_full and detail.get("description"):
                    app.description_full = detail["description"]

                if not app.description_short and detail.get("short"):
                    app.description_short = detail["short"]

                if app.downloads is None:
                    app.downloads = detail.get("installs_exact") or detail.get("downloads")

                if app.revenue is None:
                    app.revenue = detail.get("revenue")

                if app.rating is None:
                    app.rating = detail.get("rating_value")

                if app.rating_count is None:
                    app.rating_count = detail.get("rating_count")

                if app.review_count is None:
                    app.review_count = detail.get("review_count")

                logger.info(
                    "Enriched %s: languages=%s, top_dl=%s, top_rev=%s",
                    app.name,
                    app.available_languages[:3] if app.available_languages else None,
                    app.top_countries_downloads[:3] if app.top_countries_downloads else None,
                    app.top_countries_revenue[:3] if app.top_countries_revenue else None,
                )

            except Exception as exc:
                logger.warning(
                    "Failed to enrich %s (%s): %s — skipping",
                    app.name, app.app_id, exc,
                )

            enriched.append(app)

        return enriched

    # ------------------------------------------------------------------
    # Normalize
    # ------------------------------------------------------------------

    def _normalize(
        self,
        raw: dict,
        rank: int,
        store: StoreType,
        country: str,
        language: str,
    ) -> NormalizedApp:
        """Map raw AppstoreSpy response fields → NormalizedApp.

        Field names are taken directly from the OpenAPI PlayApp / IosApp schemas.
        """
        if store == StoreType.GOOGLE_PLAY:
            return NormalizedApp(
                rank=rank,
                app_id=raw.get("bundle") or str(raw.get("id", "")),
                name=raw.get("name", ""),
                developer_name=raw.get("developer_name"),
                category=raw.get("category"),
                description_short=raw.get("short"),
                description_full=raw.get("description"),
                rating=raw.get("rating_value"),
                rating_count=raw.get("rating_count"),
                review_count=raw.get("review_count"),
                downloads=raw.get("installs_exact"),
                downloads_month=raw.get("downloads"),
                downloads_lifetime=None,  # PlayApp doesn't have this field
                revenue=raw.get("revenue"),
                revenue_month=None,
                revenue_lifetime=None,
                iap=raw.get("iap"),
                update_date=raw.get("updated"),
                release_date=raw.get("released"),
                version=raw.get("version"),
                icon=raw.get("icon"),
                available_languages=raw.get("languages"),
                top_countries_downloads=raw.get("top_countries_downloads"),
                top_countries_revenue=raw.get("top_countries_revenue"),
                country=country,
                language=language,
                store=store,
            )
        else:
            # IosApp schema field mapping
            return NormalizedApp(
                rank=rank,
                app_id=str(raw.get("id", "")) or raw.get("bundle", ""),
                name=raw.get("name", ""),
                developer_name=raw.get("developer_name"),
                category=(
                    ", ".join(raw["category"])
                    if isinstance(raw.get("category"), list)
                    else raw.get("category")
                ),
                description_short=raw.get("short"),
                description_full=raw.get("description"),
                rating=raw.get("rating_value"),
                rating_count=raw.get("rating_count"),
                review_count=raw.get("review_count"),
                downloads=raw.get("downloads"),
                downloads_month=None,
                downloads_lifetime=None,
                revenue=raw.get("revenue"),
                revenue_month=None,
                revenue_lifetime=None,
                iap=raw.get("iap"),
                update_date=raw.get("updated"),
                release_date=raw.get("released"),
                version=raw.get("version"),
                icon=raw.get("icon"),
                available_languages=raw.get("languages"),
                top_countries_downloads=raw.get("top_countries_downloads"),
                top_countries_revenue=raw.get("top_countries_revenue"),
                country=country,
                language=language,
                store=store,
            )

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    def _handle_status(self, response: httpx.Response) -> None:
        """Interpret AppstoreSpy HTTP status codes."""
        status = response.status_code

        if status == 200:
            return

        if status == 202:
            raise AppstoreSpyError(
                "App chưa có dữ liệu đầy đủ trong AppstoreSpy. "
                "API đã submit app cho crawling.",
                status_code=202,
            )
        if status == 204:
            raise AppstoreSpyError(
                "Không có dữ liệu cho country được chọn.", status_code=204
            )
        if status == 403:
            raise AppstoreSpyError(
                "AppstoreSpy API key không hợp lệ.", status_code=403
            )
        if status == 429:
            raise AppstoreSpyError(
                "AppstoreSpy rate limit — vui lòng thử lại sau.", status_code=429
            )

        raise AppstoreSpyError(
            f"AppstoreSpy trả lỗi HTTP {status}: {response.text[:200]}",
            status_code=status,
        )

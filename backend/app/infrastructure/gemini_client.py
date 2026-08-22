"""Gemini API client for market research analysis.

Uses google-genai SDK. Sends factual AppstoreSpy data and receives
structured JSON that is validated with Pydantic before use.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Optional

from google import genai
from google.genai import types as genai_types

from app.domain.models import NormalizedApp
from app.domain.schemas import GeminiAnalysisResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System instruction (per spec section 17)
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTION = """\
You are a senior mobile app market researcher.

You must analyze ONLY the factual data supplied by the application.

Never invent:
- download numbers
- revenue numbers
- ratings
- review counts
- developer names
- app features
- market statistics

If a specific insight is not explicitly present in the source data, use your expertise as a senior researcher to make logical qualitative inferences based on the app's category, description, and available metrics. Do NOT state that data is unavailable or cannot be verified.

DO NOT use prefixes like "FACT:", "INFERENCE:", or "RECOMMENDATION:" in your text. Integrate them naturally.

The final answer must be valid JSON matching the provided schema.

The output will be written automatically into an Excel template, so:
- do not return Markdown
- do not return code fences
- do not add commentary outside JSON
- preserve the exact JSON keys
- write concise but useful Vietnamese analysis
"""

# ---------------------------------------------------------------------------
# User prompt template (per spec section 17)
# ---------------------------------------------------------------------------

USER_PROMPT_TEMPLATE = """\
Keyword:
{keyword}

Store:
{store}

Country:
{country}

Below is the factual AppstoreSpy data for the top {n} search results:

{apps_json}

Analyze these competitors and produce the requested Market Research output.

The output must be valid JSON with this exact structure:
{{
  "keyword": "{keyword}",
  "market_segmentation": {{
    "geographical": {{"location": "...", "languages": "..."}},
    "demographic": {{"age": "...", "gender": "...", "income": "..."}},
    "behavioural": {{"occasions": "...", "usage_rate": "...", "benefits_sought": "...", "loyalty": "..."}},
    "psychographic": {{"values": "...", "beliefs": "...", "opinion": "...", "interests": "..."}}
  }},
  "swot": [
    {{
      "app_name": "...",
      "strengths": "...",
      "weakness": "...",
      "ip_copyright": "...",
      "gambling_policy": "...",
      "data_providers": "..."
    }}
  ],
  "customer_personas": {{
    "device": "...",
    "age": "...",
    "needs": "...",
    "painpoint": "...",
    "must_have": "...",
    "emotional_state": "..."
  }},
  "problem_statement": {{
    "user": "...",
    "problem": "...",
    "context": "...",
    "statement": "..."
  }},
  "product_idea": {{
    "problem": "...",
    "vision": "...",
    "goal": "...",
    "target_audience": "...",
    "strategy": "...",
    "feature": "..."
  }}
}}

Important:
- Do not invent numerical data.
- When discussing competitor strengths/weaknesses, base the analysis on supplied metadata, description, and logical inference.
- If a specific feature or qualitative data point is missing, infer it logically based on the context. Do NOT use phrases like "Không đủ dữ liệu xác minh" hoặc "Không có thông tin".
- For Geographical Location: Must prioritize listing specific countries from "top_countries_downloads" and "top_countries_revenue". Avoid generic words like "Toàn cầu" or "Worldwide" if specific country codes exist.
- For Languages: Must prioritize listing specific languages from "available_languages". Avoid generic words like "Nhiều ngôn ngữ" if specific languages are provided.
- Make the qualitative analysis in Customer Personas, Problem Statement, and Product Idea highly specific to the {keyword} and the analyzed competitors, rather than overly generic templates.
- The SWOT array must contain exactly one entry per app ({n} entries total).
- Return JSON only — no markdown, no code fences, no extra text.
"""

RETRY_PROMPT = """\
Your previous response did not conform to the required JSON schema.

Return ONLY valid JSON matching the schema.

Do not add markdown fences.
"""


class GeminiError(Exception):
    """Error communicating with Gemini API."""
    pass


class GeminiClient:
    """Client for Google Gemini generative AI analysis."""

    def __init__(self, api_key: str, max_retries: int = 2):
        self._api_key = api_key
        self._max_retries = max_retries
        self._client = genai.Client(api_key=api_key)

    async def analyze(
        self,
        keyword: str,
        store: str,
        country: str,
        apps: list[NormalizedApp],
    ) -> GeminiAnalysisResult:
        """Send app data to Gemini and get validated analysis."""

        # Build factual app data JSON (exclude sensitive/irrelevant fields)
        apps_data = []
        for app in apps:
            apps_data.append({
                "rank": app.rank,
                "app_id": app.app_id,
                "name": app.name,
                "developer_name": app.developer_name,
                "category": app.category,
                "description_short": app.description_short,
                "description_full": app.description_full,
                "rating": app.rating,
                "rating_count": app.rating_count,
                "review_count": app.review_count,
                "downloads": app.downloads,
                "downloads_month": app.downloads_month,
                "revenue": app.revenue,
                "iap": app.iap,
                "update_date": app.update_date,
                "release_date": app.release_date,
                "version": app.version,
                "available_languages": app.available_languages,
                "top_countries_downloads": app.top_countries_downloads,
                "top_countries_revenue": app.top_countries_revenue,
            })

        apps_json = json.dumps(apps_data, indent=2, ensure_ascii=False)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            keyword=keyword,
            store=store,
            country=country,
            n=len(apps),
            apps_json=apps_json,
        )

        # First attempt
        raw_text = await self._call_gemini(user_prompt)
        result = self._try_parse(raw_text)

        if result is not None:
            return result

        # Retry loop
        for attempt in range(1, self._max_retries + 1):
            logger.warning(
                "Gemini JSON invalid, retry %d/%d", attempt, self._max_retries
            )
            retry_prompt = f"{user_prompt}\n\n{RETRY_PROMPT}"
            raw_text = await self._call_gemini(retry_prompt)
            result = self._try_parse(raw_text)
            if result is not None:
                return result

        raise GeminiError(
            "Gemini không trả về JSON hợp lệ sau "
            f"{self._max_retries + 1} lần thử."
        )

    async def _call_gemini(self, user_prompt: str) -> str:
        """Call Gemini API and return raw text response, with retry for 503 errors."""
        import asyncio
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                response = await self._client.aio.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=user_prompt,
                    config=genai_types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.3,
                        max_output_tokens=8192,
                    ),
                )
                text = response.text or ""
                logger.info("Gemini response length: %d chars", len(text))
                return text
            except Exception as exc:
                error_str = str(exc)
                if "503" in error_str and attempt < max_attempts:
                    logger.warning("Gemini 503 UNAVAILABLE (attempt %d/%d). Retrying in 3s...", attempt, max_attempts)
                    await asyncio.sleep(3)
                    continue
                
                logger.error("Gemini API error: %s", exc)
                raise GeminiError(f"Gemini API error: {exc}") from exc
        
        raise GeminiError("Gemini API error: max retries reached for 503 UNAVAILABLE")

    def _try_parse(self, raw_text: str) -> Optional[GeminiAnalysisResult]:
        """Try to parse Gemini response as JSON and validate with Pydantic."""
        # Strip markdown code fences if present
        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.warning("Gemini returned invalid JSON: %s", exc)
            return None

        try:
            result = GeminiAnalysisResult.model_validate(data)
            return result
        except Exception as exc:
            logger.warning("Gemini JSON failed Pydantic validation: %s", exc)
            return None

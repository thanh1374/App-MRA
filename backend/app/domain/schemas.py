"""Pydantic schemas for Gemini output validation.

These schemas define the *exact* JSON structure Gemini must return.
Any response that does not conform triggers a retry (up to GEMINI_MAX_RETRIES).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Market Segmentation
# ---------------------------------------------------------------------------

class GeographicalSegment(BaseModel):
    location: str = ""
    languages: str = ""


class DemographicSegment(BaseModel):
    age: str = ""
    gender: str = ""
    income: str = ""


class BehaviouralSegment(BaseModel):
    occasions: str = ""
    usage_rate: str = ""
    benefits_sought: str = ""
    loyalty: str = ""


class PsychographicSegment(BaseModel):
    values: str = ""
    beliefs: str = ""
    opinion: str = ""
    interests: str = ""


class MarketSegmentation(BaseModel):
    geographical: GeographicalSegment = Field(default_factory=GeographicalSegment)
    demographic: DemographicSegment = Field(default_factory=DemographicSegment)
    behavioural: BehaviouralSegment = Field(default_factory=BehaviouralSegment)
    psychographic: PsychographicSegment = Field(default_factory=PsychographicSegment)


# ---------------------------------------------------------------------------
# SWOT
# ---------------------------------------------------------------------------

class SwotEntry(BaseModel):
    app_name: str = ""
    strengths: str = ""
    weakness: str = ""
    ip_copyright: str = ""
    gambling_policy: str = ""
    data_providers: str = ""


# ---------------------------------------------------------------------------
# Customer Personas
# ---------------------------------------------------------------------------

class CustomerPersonas(BaseModel):
    device: str = ""
    age: str = ""
    needs: str = ""
    painpoint: str = ""
    must_have: str = ""
    emotional_state: str = ""


# ---------------------------------------------------------------------------
# Problem Statement
# ---------------------------------------------------------------------------

class ProblemStatement(BaseModel):
    user: str = ""
    problem: str = ""
    context: str = ""
    statement: str = ""


# ---------------------------------------------------------------------------
# Product Idea
# ---------------------------------------------------------------------------

class ProductIdea(BaseModel):
    problem: str = ""
    vision: str = ""
    goal: str = ""
    target_audience: str = ""
    strategy: str = ""
    feature: str = ""


# ---------------------------------------------------------------------------
# Top-level Gemini Analysis Result
# ---------------------------------------------------------------------------

class GeminiAnalysisResult(BaseModel):
    """Top-level schema that Gemini must return as valid JSON."""

    keyword: str = ""
    market_segmentation: MarketSegmentation = Field(
        default_factory=MarketSegmentation
    )
    swot: list[SwotEntry] = Field(default_factory=list)
    customer_personas: CustomerPersonas = Field(default_factory=CustomerPersonas)
    problem_statement: ProblemStatement = Field(default_factory=ProblemStatement)
    product_idea: ProductIdea = Field(default_factory=ProductIdea)

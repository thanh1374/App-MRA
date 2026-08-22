"""Excel cell mapping — maps Gemini JSON keys to exact Excel cells.

Based on actual Template.xlsx analysis:
- Sheet: 'Template'
- Market Segmentation: rows 3-15, labels in C, values in D (merged D:J)
- SWOT: rows 21-25, app_name in B, strengths in C, weakness in D
- Threats: rows 30-33, ip_copyright in B, gambling_policy in C, data_providers in D
- Customer Personas: rows 40-45, labels in B, values in C (merged C:F)
- Problem Statement: row 50 headers, row 51 values (B=User, C=Problem, D=Context)
- Product Idea: rows 56-58 (B=User first, C=Job to be done, D=Outcome)
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Market Segmentation → column D (merged D:J)
# Template structure:
#   B3:B4 = "Geographycal" (merged)
#   C3 = Location,   D3 = value (merged D3:J3)
#   C4 = Language(s), D4 = value (merged D4:J4)
#   B5:B7 = "Demographic" (merged)
#   C5 = Age,    D5 = value (merged D5:J5)
#   C6 = Gender, D6 = value (merged D6:J6)
#   C7 = Income, D7 = value (merged D7:J7)
#   B8:B11 = "Behaviourial" (merged)
#   C8 = Occassions,      D8 = value (merged D8:J8)
#   C9 = Usage Rate,      D9 = value (merged D9:J9)
#   C10 = Benefits Sought, D10 = value (merged D10:J10)
#   C11 = Loyalty,         D11 = value (merged D11:J11)
#   B12:B15 = "Psychographic" (merged)
#   C12 = Values,    D12 = value (merged D12:J12)
#   C13 = Beliefs,   D13 = value (merged D13:J13)
#   C14 = Opinion,   D14 = value (merged D14:J14)
#   C15 = Interests, D15 = value (merged D15:J15)
# ---------------------------------------------------------------------------

MARKET_SEGMENTATION_MAP: dict[str, str] = {
    "market_segmentation.geographical.location": "D3",
    "market_segmentation.geographical.languages": "D4",
    "market_segmentation.demographic.age": "D5",
    "market_segmentation.demographic.gender": "D6",
    "market_segmentation.demographic.income": "D7",
    "market_segmentation.behavioural.occasions": "D8",
    "market_segmentation.behavioural.usage_rate": "D9",
    "market_segmentation.behavioural.benefits_sought": "D10",
    "market_segmentation.behavioural.loyalty": "D11",
    "market_segmentation.psychographic.values": "D12",
    "market_segmentation.psychographic.beliefs": "D13",
    "market_segmentation.psychographic.opinion": "D14",
    "market_segmentation.psychographic.interests": "D15",
}

# ---------------------------------------------------------------------------
# SWOT → rows 21-25 (5 competitors)
#   B20 = "SWOT" header, C20 = "Strengths", D20 = "Weakness"
#   B21-B25 = App name
#   C21-C25 = Strengths
#   D21-D25 = Weakness
# ---------------------------------------------------------------------------

SWOT_START_ROW = 21
SWOT_COLUMNS = {
    "app_name": "B",
    "strengths": "C",
    "weakness": "D",
}

# ---------------------------------------------------------------------------
# Threats → rows 30-33
#   B30 = "IP & Copyright", C30 = "Gambling Policy", D30 = "Data Providers"
#   B31-B33 = ip_copyright values
#   C31-C33 = gambling_policy values
#   D31-D33 = data_providers values
# ---------------------------------------------------------------------------

THREATS_START_ROW = 31
THREATS_COLUMNS = {
    "ip_copyright": "B",
    "gambling_policy": "C",
    "data_providers": "D",
}

# ---------------------------------------------------------------------------
# Customer Personas → rows 40-45, labels in B, values in C (merged C:F)
#   B40 = "Device",    C40 = value (merged C40:F40)
#   B41 = "Age",       C41 = value (merged C41:F41)
#   B42 = "Needs",     C42 = value (merged C42:F42)
#   B43 = "Painpoint", C43 = value (merged C43:F43)
#   B44 = "Must have", C44 = value (merged C44:F44)
#   B45 = "Emotional State", C45 = value (merged C45:F45)
# ---------------------------------------------------------------------------

CUSTOMER_PERSONAS_MAP: dict[str, str] = {
    "customer_personas.device": "C40",
    "customer_personas.age": "C41",
    "customer_personas.needs": "C42",
    "customer_personas.painpoint": "C43",
    "customer_personas.must_have": "C44",
    "customer_personas.emotional_state": "C45",
}

# ---------------------------------------------------------------------------
# Problem Statement → rows 50-51
#   B50 = "User", C50 = "Problem", D50 = "Context"
#   B51 = user value, C51 = problem value, D51 = context value
# ---------------------------------------------------------------------------

PROBLEM_STATEMENT_MAP: dict[str, str] = {
    "problem_statement.user": "B51",
    "problem_statement.problem": "C51",
    "problem_statement.context": "D51",
}

# ---------------------------------------------------------------------------
# Product Idea → rows 56-58
#   B56 = "User first", C56 = "Job tobe done", D56 = "Out come"
#   B57 = Problem,  C57 = Vision,   D57 = Goal
#   B58 = Target Audience, C58 = Strategy, D58 = Feature
# ---------------------------------------------------------------------------

PRODUCT_IDEA_MAP: dict[str, str] = {
    "product_idea.problem": "B57",
    "product_idea.vision": "C57",
    "product_idea.goal": "D57",
    "product_idea.target_audience": "B58",
    "product_idea.strategy": "C58",
    "product_idea.feature": "D58",
}


def get_full_mapping() -> dict[str, str]:
    """Return the complete flat mapping of JSON dotted-path → cell coordinate."""
    mapping: dict[str, str] = {}
    mapping.update(MARKET_SEGMENTATION_MAP)
    mapping.update(CUSTOMER_PERSONAS_MAP)
    mapping.update(PROBLEM_STATEMENT_MAP)
    mapping.update(PRODUCT_IDEA_MAP)
    return mapping

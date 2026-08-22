"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analyze, export, health
from app.config.settings import settings
from app.utils.logging_config import setup_logging

# Initialize logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="App Market Research Analyzer",
    description="Analyze mobile app market using AppstoreSpy + Gemini AI",
    version="1.0.0",
)

# CORS — only allow configured frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(export.router)

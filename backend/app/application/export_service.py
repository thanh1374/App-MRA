"""Export service — generates Excel from stored analysis."""

from __future__ import annotations

import logging
from pathlib import Path

from app.application.analyze_service import get_job
from app.config.settings import settings
from app.domain.schemas import GeminiAnalysisResult
from app.infrastructure.excel.excel_writer import ExcelWriter

logger = logging.getLogger(__name__)


def export_excel(job_id: str) -> Path:
    """Generate Excel file for a completed analysis job.

    Returns the path to the generated .xlsx file.
    """
    job = get_job(job_id)
    if job is None:
        raise ValueError(f"Job '{job_id}' không tồn tại.")

    if job.status != "completed":
        raise ValueError(f"Job '{job_id}' chưa hoàn thành (status: {job.status}).")

    if job.analysis is None:
        raise ValueError(f"Job '{job_id}' không có dữ liệu phân tích.")

    # Reconstruct validated Pydantic model from stored dict
    analysis = GeminiAnalysisResult.model_validate(job.analysis)

    # Resolve template path (relative to project root)
    template_path = Path(settings.template_path)
    if not template_path.is_absolute():
        # Go up from backend/ to project root
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        template_path = project_root / template_path

    output_dir = Path(settings.output_dir)
    if not output_dir.is_absolute():
        import os
        if os.environ.get("VERCEL"):
            output_dir = Path("/tmp") / settings.output_dir
        else:
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            output_dir = project_root / output_dir

    writer = ExcelWriter(
        template_path=template_path,
        output_dir=output_dir,
    )

    output_path = writer.write(
        analysis=analysis,
        keyword=job.keyword,
    )

    logger.info("Excel exported: %s", output_path)
    return output_path

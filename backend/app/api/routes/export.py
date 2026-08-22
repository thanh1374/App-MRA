"""Export endpoint — generates Excel and returns file download."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.api.schemas import ExportRequest
from app.application.export_service import export_excel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/export")
async def export(request: ExportRequest):
    """Generate and download the Excel report.

    Returns the .xlsx file as a downloadable attachment.
    """
    try:
        output_path = export_excel(request.job_id)

        return FileResponse(
            path=str(output_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=output_path.name,
        )

    except ValueError as exc:
        logger.error("Export error: %s", exc)
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "EXPORT_ERROR",
                "message": str(exc),
            },
        )

    except FileNotFoundError as exc:
        logger.error("Template not found: %s", exc)
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "TEMPLATE_MISSING",
                "message": "Excel template không tồn tại.",
            },
        )

    except Exception as exc:
        logger.exception("Unexpected export error")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "EXCEL_ERROR",
                "message": "Không thể tạo Excel từ template.",
            },
        )

import type { AnalyzeRequest, AnalyzeResponse } from "../types";

const API_BASE_URL = "http://localhost:8000/api";

export class ApiError extends Error {
  public code: string;
  constructor(message: string, code: string) {
    super(message);
    this.code = code;
  }
}

export const analyzeKeyword = async (request: AnalyzeRequest): Promise<AnalyzeResponse> => {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message = errorData.detail?.message || "Lỗi kết nối đến máy chủ.";
    const code = errorData.detail?.error_code || "UNKNOWN_ERROR";
    throw new ApiError(message, code);
  }

  return response.json();
};

export const exportExcel = async (jobId: string, keyword: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/export`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ job_id: jobId }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message = errorData.detail?.message || "Lỗi xuất file Excel.";
    const code = errorData.detail?.error_code || "EXPORT_ERROR";
    throw new ApiError(message, code);
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  
  const dateStr = new Date().toISOString().replace(/[:T-]/g, "").slice(0, 14);
  a.download = `market_research_${keyword.replace(/[^a-zA-Z0-9]/g, "_")}_${dateStr}.xlsx`;
  
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
};

import { useState } from "react";
import { Sparkles } from "lucide-react";
import type { AnalyzeRequest, AnalyzeResponse } from "./types";
import { analyzeKeyword, exportExcel, ApiError } from "./services/api";
import Sidebar from "./components/Sidebar";
import AnalyzeForm from "./components/AnalyzeForm";
import ProgressIndicator from "./components/ProgressIndicator";
import ErrorState from "./components/ErrorState";
import ResultsPanel from "./components/ResultsPanel";

type AppState = "idle" | "loading" | "success" | "error";
type Page = "new-analysis" | "results";

function App() {
  const [state, setState] = useState<AppState>("idle");
  const [page, setPage] = useState<Page>("new-analysis");
  const [errorMsg, setErrorMsg] = useState<string>("");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [resultsCount, setResultsCount] = useState(0);

  const handleAnalyze = async (request: AnalyzeRequest) => {
    setState("loading");
    setErrorMsg("");
    setResult(null);

    try {
      const res = await analyzeKeyword(request);
      setResult(res);
      setResultsCount((prev) => prev + 1);
      setState("success");
      setPage("results");
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg("Có lỗi không xác định xảy ra.");
      }
      setState("error");
    }
  };

  const handleExport = async (jobId: string, keyword: string) => {
    try {
      await exportExcel(jobId, keyword);
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        alert(err.message);
      } else {
        alert("Lỗi khi xuất file Excel.");
      }
    }
  };

  const handleRetry = () => {
    setState("idle");
    setPage("new-analysis");
  };

  const handleNavigate = (targetPage: Page) => {
    if (targetPage === "results" && !result) return;
    setPage(targetPage);
    if (targetPage === "new-analysis" && state !== "loading") {
      setState("idle");
    }
  };

  // Determine which page content to show
  const isAnalysisFlow = page === "new-analysis" || state === "loading" || state === "error";

  return (
    <div className="app-layout">
      <Sidebar
        activePage={isAnalysisFlow ? "new-analysis" : "results"}
        onNavigate={handleNavigate}
        resultsCount={resultsCount}
      />

      {/* Main Content */}
      {state === "loading" || state === "error" ? (
        <div className="main-content-centered">
          {state === "loading" && <ProgressIndicator />}
          {state === "error" && (
            <ErrorState message={errorMsg} onRetry={handleRetry} />
          )}
        </div>
      ) : page === "results" && result ? (
        <main className="main-content">
          <ResultsPanel
            result={result}
            onExport={() => handleExport(result.job_id, result.keyword)}
          />
        </main>
      ) : (
        <main className="main-content main-content-centered">
          <div className="content-container" style={{ width: '100%', transform: 'translateY(-15vh)' }}>
            {/* Page Header */}
            <div className="page-header-btn">
              <Sparkles />
              <span>Analysis</span>
            </div>

            {/* Form */}
            <AnalyzeForm
              onSubmit={handleAnalyze}
              isLoading={false}
            />
          </div>
        </main>
      )}
    </div>
  );
}

export default App;

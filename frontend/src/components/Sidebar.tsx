import {
  Activity,
  Sparkles,
  BarChart3,
} from "lucide-react";

type Page = "new-analysis" | "results";

interface Props {
  activePage: Page;
  onNavigate: (page: Page) => void;
  resultsCount: number;
}

export default function Sidebar({ activePage, onNavigate, resultsCount }: Props) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        {/* Logo */}
        <div className="logo-area">
          <div className="logo-icon">
            <Activity />
          </div>
          <span className="logo-text">MRA</span>
        </div>

        {/* Navigation */}
        <nav className="nav-list">
          <button
            className={`nav-item ${activePage === "new-analysis" ? "active" : ""}`}
            onClick={() => onNavigate("new-analysis")}
          >
            <Sparkles />
            <span>Phân tích mới</span>
          </button>

          <button
            className={`nav-item ${activePage === "results" ? "active" : ""}`}
            onClick={() => onNavigate("results")}
          >
            <BarChart3 />
            <span>Kết quả</span>
            {resultsCount > 0 && (
              <span className="nav-badge">{resultsCount}</span>
            )}
          </button>

        </nav>
      </div>

      <div className="sidebar-bottom">
        <span style={{ fontSize: '12px', color: 'var(--text-tertiary)', textAlign: 'center', opacity: 0.9 }}>
          Developer: ThanhDN
          thanhdn@pandaglobal.com.vn
        </span>
      </div>
    </aside>
  );
}

import { useState } from "react";
import { BarChart3, Download } from "lucide-react";
import type { AnalyzeResponse } from "../types";
import AppCard from "./AppCard";
import {
  SegmentationTab,
  SwotTab,
  PersonasTab,
  ProblemTab,
  ProductTab,
} from "./TabContent";

interface Props {
  result: AnalyzeResponse;
  onExport: () => void;
}

type TabType = "segmentation" | "swot" | "personas" | "problem" | "product";

const tabs: { id: TabType; label: string }[] = [
  { id: "segmentation", label: "Segmentation" },
  { id: "swot", label: "SWOT" },
  { id: "personas", label: "Personas" },
  { id: "problem", label: "Problem" },
  { id: "product", label: "Product" },
];

export default function ResultsPanel({ result, onExport }: Props) {
  const [activeTab, setActiveTab] = useState<TabType>("segmentation");
  const ana = result.analysis;

  const storeLabel = result.store === "google_play" ? "Google Play" : "App Store";

  return (
    <div className="results-container animate-in">
      {/* Results Header */}
      <div className="results-header">
        <div className="header-left">
          <div className="page-header-btn">
            <BarChart3 />
            <span>Results</span>
          </div>
          <div className="meta-row">
            <span className="meta-pill">{storeLabel}</span>
            <span className="meta-pill">{result.country}</span>
            <span className="meta-pill">{result.apps.length} ứng dụng</span>
          </div>
        </div>
        <button className="export-btn" onClick={onExport}>
          <Download size={16} />
          Xuất excel
        </button>
      </div>

      {/* Top 5 Competitors */}
      <div className="competitors-section">
        <span className="competitors-label">TOP 5 ĐỐI THỦ</span>
        <div className="cards-row">
          {result.apps.map((app, i) => (
            <div key={app.app_id} className={`stagger-${i + 1}`}>
              <AppCard app={app} store={result.store} />
            </div>
          ))}
        </div>
      </div>

      {/* Tab Bar + Content */}
      {ana && (
        <div className="tab-bar-section">
          <div className="tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                className={`tab-item ${activeTab === tab.id ? "active" : ""}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div style={{ marginTop: "var(--space-8)" }}>
            {activeTab === "segmentation" && (
              <SegmentationTab data={ana.market_segmentation} />
            )}
            {activeTab === "swot" && <SwotTab data={ana.swot} />}
            {activeTab === "personas" && <PersonasTab data={ana.customer_personas} />}
            {activeTab === "problem" && <ProblemTab data={ana.problem_statement} />}
            {activeTab === "product" && <ProductTab data={ana.product_idea} />}
          </div>
        </div>
      )}
    </div>
  );
}

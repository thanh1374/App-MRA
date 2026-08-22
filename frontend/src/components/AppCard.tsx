import { Star, ArrowDownCircle } from "lucide-react";
import type { AppSummary, StoreType } from "../types";

interface Props {
  app: AppSummary;
  store: StoreType;
}

export default function AppCard({ app, store }: Props) {
  const formatNumber = (num?: number) => {
    if (num == null) return "N/A";
    if (num >= 1000000) return Math.floor(num / 1000000) + "M+";
    if (num >= 1000) return Math.floor(num / 1000) + "K+";
    return num.toString();
  };

  const appUrl = store === "google_play" 
    ? `https://play.google.com/store/apps/details?id=${app.app_id}`
    : `https://apps.apple.com/app/id${app.app_id}`;

  return (
    <a href={appUrl} target="_blank" rel="noreferrer" className="competitor-card animate-in" style={{ textDecoration: 'none', color: 'inherit', display: 'flex' }}>
      {/* Rank Badge */}
      <div className="rank-badge">{app.rank}</div>

      {/* App Icon */}
      {app.icon ? (
        <img
          src={app.icon}
          alt={app.name}
          className="app-icon"
          loading="lazy"
        />
      ) : (
        <div className="app-icon" style={{ display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-tertiary)", fontSize: "12px" }}>
          N/A
        </div>
      )}

      {/* App Info */}
      <div className="app-info">
        <div className="app-name" title={app.name}>{app.name}</div>
        <div className="app-developer" title={app.developer_name}>
          {app.developer_name || "Unknown"}
        </div>
      </div>

      {/* Stats */}
      <div className="stats">
        <div className="stat-row rating">
          <Star size={14} fill="currentColor" />
          <span>{app.rating ? app.rating.toFixed(1) : "N/A"}</span>
        </div>
        <div className="stat-row downloads">
          <ArrowDownCircle size={14} />
          <span>{formatNumber(app.downloads)}</span>
        </div>
      </div>
    </a>
  );
}

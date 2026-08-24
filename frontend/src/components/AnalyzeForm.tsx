import { useState } from "react";
import { Search, ShoppingBag, Globe, Languages, ChevronDown, Loader2, Rocket, Info } from "lucide-react";
import type { AnalyzeRequest, StoreType } from "../types";

interface Props {
  onSubmit: (req: AnalyzeRequest) => void;
  isLoading: boolean;
}

export default function AnalyzeForm({ onSubmit, isLoading }: Props) {
  const [keyword, setKeyword] = useState("");
  const [store, setStore] = useState<StoreType>("google_play");
  const [country, setCountry] = useState("US");
  const [language, setLanguage] = useState("en_US");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyword.trim() || isLoading) return;

    onSubmit({
      keyword: keyword.trim(),
      store,
      country,
      language,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-card">
        {/* Hero Search Input */}
        <div className="search-input-container">
          <Search />
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="Nhập keyword để phân tích..."
            disabled={isLoading}
          />
        </div>

        <div className="form-spacer" />

        {/* Dropdowns Row */}
        <div className="dropdowns-row">
          {/* Store */}
          <div className="select-field">
            <ShoppingBag />
            <select
              value={store}
              onChange={(e) => setStore(e.target.value as StoreType)}
              disabled={isLoading}
            >
              <option value="google_play">Google Play</option>
              <option value="app_store">App Store</option>
            </select>
            <ChevronDown className="chevron" />
          </div>

          {/* Country */}
          <div className="select-field">
            <Globe />
            <select
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              disabled={isLoading}
            >
              <option value="US">United States</option>
              <option value="VN">Vietnam</option>
              <option value="GB">United Kingdom</option>
              <option value="JP">Japan</option>
              <option value="KR">South Korea</option>
              <option value="IN">India</option>
            </select>
            <ChevronDown className="chevron" />
          </div>

          {/* Language */}
          <div className="select-field">
            <Languages />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              disabled={isLoading}
            >
              <option value="en_US">English</option>
              <option value="vi">Vietnamese</option>
              <option value="ja">Japanese</option>
              <option value="ko">Korean</option>
            </select>
            <ChevronDown className="chevron" />
          </div>
        </div>



        <div className="form-spacer-lg" />

        {/* CTA Button */}
        <button
          type="submit"
          className="cta-button"
          disabled={isLoading || !keyword.trim()}
        >
          {isLoading ? (
            <>
              <Loader2 className="spinner-icon" />
              Đang phân tích...
            </>
          ) : (
            <>
              <Rocket size={16} />
              Bắt đầu phân tích
            </>
          )}
        </button>
      </div>

      {/* Quick Tips */}
      <div className="form-spacer" />
      <div className="quick-tips">
        <Info />
        <span>Mẹo: Nhập từ khóa cụ thể để nhận kết quả phân tích chính xác hơn</span>
      </div>
    </form>
  );
}

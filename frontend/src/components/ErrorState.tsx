import { AlertTriangle } from "lucide-react";

interface Props {
  message: string;
  onRetry: () => void;
}

export default function ErrorState({ message, onRetry }: Props) {
  return (
    <div className="error-card animate-in">
      <div className="error-icon">
        <AlertTriangle />
      </div>
      <h3 className="error-title">Phân tích thất bại</h3>
      <p className="error-message">
        {message || "Không thể kết nối. Vui lòng kiểm tra API keys và thử lại."}
      </p>
      <button className="retry-btn" onClick={onRetry}>
        Thử lại
      </button>
    </div>
  );
}

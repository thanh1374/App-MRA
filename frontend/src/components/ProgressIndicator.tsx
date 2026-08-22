import { CheckCircle, Loader2 } from "lucide-react";

interface Props {
  currentStep?: number;
  statusText?: string;
}

export default function ProgressIndicator({
  currentStep = 1,
  statusText = "Đang thu thập dữ liệu...",
}: Props) {
  const steps = [
    { label: "Research", step: 1 },
    { label: "Analyzing", step: 2 },
    { label: "Report", step: 3 },
  ];

  const progressPercent = Math.min((currentStep / steps.length) * 100, 100);

  return (
    <div className="loading-card animate-in">
      {/* Spinner */}
      <div className="spinner-ring" />

      <div className="form-spacer" />

      {/* Status Text */}
      <p className="loading-status-text">{statusText}</p>

      <div className="form-spacer" />

      {/* Progress Bar */}
      <div className="progress-container">
        <div className="progress-bar-bg">
          <div
            className="progress-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <span className="progress-step-text">
          Step {currentStep}/{steps.length}
        </span>
      </div>

      <div className="form-spacer-lg" />

      {/* Step Checklist */}
      <div className="step-checklist">
        {steps.map(({ label, step }) => {
          let status: "completed" | "active" | "pending" = "pending";
          if (step < currentStep) status = "completed";
          else if (step === currentStep) status = "active";

          return (
            <div key={step} className={`checklist-item ${status}`}>
              {status === "completed" && <CheckCircle size={16} />}
              {status === "active" && <Loader2 size={16} />}
              {status === "pending" && <div className="pending-circle" />}
              <span>{label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

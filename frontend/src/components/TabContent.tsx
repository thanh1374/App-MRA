import {
  Smartphone,
  Calendar,
  Heart,
  AlertCircle,
  Star,
  SmilePlus,
  Target,
  Eye,
  Goal,
  Users,
  Map,
  Lightbulb,
  Globe,
  Brain,
  User,
  AlertTriangle,
  Search,
  FileText,
} from "lucide-react";
import type {
  MarketSegmentation,
  SwotEntry,
  CustomerPersonas,
  ProblemStatement,
  ProductIdea,
} from "../types";

interface SegmentationProps {
  data: MarketSegmentation;
}

export function SegmentationTab({ data }: SegmentationProps) {
  return (
    <div className="tab-content">
      <div className="persona-list">
        <div className="persona-row animate-in stagger-1">
          <div className="persona-icon-circle"><Globe /></div>
          <div className="persona-details">
            <span className="persona-label">Geographical</span>
            <div className="persona-value">
              <div><strong>Location:</strong> {data.geographical.location}</div>
              <div style={{ marginTop: '4px' }}><strong>Languages:</strong> {data.geographical.languages}</div>
            </div>
          </div>
        </div>

        <div className="persona-row animate-in stagger-2">
          <div className="persona-icon-circle"><Users /></div>
          <div className="persona-details">
            <span className="persona-label">Demographic</span>
            <div className="persona-value">
              <div><strong>Age:</strong> {data.demographic.age}</div>
              <div style={{ marginTop: '4px' }}><strong>Gender:</strong> {data.demographic.gender}</div>
              <div style={{ marginTop: '4px' }}><strong>Income:</strong> {data.demographic.income}</div>
            </div>
          </div>
        </div>

        <div className="persona-row animate-in stagger-3">
          <div className="persona-icon-circle"><Target /></div>
          <div className="persona-details">
            <span className="persona-label">Behavioural</span>
            <div className="persona-value">
              <div><strong>Occasions:</strong> {data.behavioural.occasions}</div>
              <div style={{ marginTop: '4px' }}><strong>Usage Rate:</strong> {data.behavioural.usage_rate}</div>
              <div style={{ marginTop: '4px' }}><strong>Benefits:</strong> {data.behavioural.benefits_sought}</div>
              <div style={{ marginTop: '4px' }}><strong>Loyalty:</strong> {data.behavioural.loyalty}</div>
            </div>
          </div>
        </div>

        <div className="persona-row animate-in stagger-4">
          <div className="persona-icon-circle"><Brain /></div>
          <div className="persona-details">
            <span className="persona-label">Psychographic</span>
            <div className="persona-value">
              <div><strong>Values:</strong> {data.psychographic.values}</div>
              <div style={{ marginTop: '4px' }}><strong>Beliefs:</strong> {data.psychographic.beliefs}</div>
              <div style={{ marginTop: '4px' }}><strong>Opinion:</strong> {data.psychographic.opinion}</div>
              <div style={{ marginTop: '4px' }}><strong>Interests:</strong> {data.psychographic.interests}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

interface SwotProps {
  data: SwotEntry[];
}

export function SwotTab({ data }: SwotProps) {
  return (
    <div className="tab-content">
      <div className="swot-table-container animate-in">
        <table className="swot-table">
          <thead>
            <tr>
              <th>App Name</th>
              <th>Strengths</th>
              <th>Weakness</th>
              <th>IP/Copyright</th>
              <th>Gambling Policy</th>
              <th>Data Providers</th>
            </tr>
          </thead>
          <tbody>
            {data.map((entry, i) => (
              <tr key={i} className={`animate-in stagger-${i + 1}`}>
                <td>{entry.app_name}</td>
                <td>{entry.strengths}</td>
                <td>{entry.weakness}</td>
                <td>{entry.ip_copyright}</td>
                <td>{entry.gambling_policy}</td>
                <td>{entry.data_providers}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

interface PersonasProps {
  data: CustomerPersonas;
}

const personaFields: {
  key: keyof CustomerPersonas;
  label: string;
  icon: React.ComponentType<{ size?: number }>;
}[] = [
  { key: "device", label: "Device", icon: Smartphone },
  { key: "age", label: "Age", icon: Calendar },
  { key: "needs", label: "Needs", icon: Heart },
  { key: "painpoint", label: "Pain Points", icon: AlertCircle },
  { key: "must_have", label: "Must-Have Features", icon: Star },
  { key: "emotional_state", label: "Emotional State", icon: SmilePlus },
];

export function PersonasTab({ data }: PersonasProps) {
  return (
    <div className="tab-content">
      <div className="persona-list">
        {personaFields.map(({ key, label, icon: Icon }, i) => (
          <div key={key} className={`persona-row animate-in stagger-${i + 1}`}>
            <div className="persona-icon-circle">
              <Icon />
            </div>
            <div className="persona-details">
              <span className="persona-label">{label}</span>
              <span className="persona-value">{data[key]}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

interface ProblemProps {
  data: ProblemStatement;
}

export function ProblemTab({ data }: ProblemProps) {
  return (
    <div className="tab-content">
      <div className="persona-list">
        <div className="persona-row animate-in stagger-1">
          <div className="persona-icon-circle"><User /></div>
          <div className="persona-details">
            <span className="persona-label">User</span>
            <span className="persona-value">{data.user}</span>
          </div>
        </div>
        <div className="persona-row animate-in stagger-2">
          <div className="persona-icon-circle"><AlertTriangle /></div>
          <div className="persona-details">
            <span className="persona-label">Problem</span>
            <span className="persona-value">{data.problem}</span>
          </div>
        </div>
        <div className="persona-row animate-in stagger-3">
          <div className="persona-icon-circle"><Search /></div>
          <div className="persona-details">
            <span className="persona-label">Context</span>
            <span className="persona-value">{data.context}</span>
          </div>
        </div>
        <div className="persona-row animate-in stagger-4">
          <div className="persona-icon-circle"><FileText /></div>
          <div className="persona-details">
            <span className="persona-label">Full Statement</span>
            <span className="persona-value">{data.statement}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

interface ProductProps {
  data: ProductIdea;
}

const productFields: {
  key: keyof ProductIdea;
  label: string;
  icon: React.ComponentType<{ size?: number }>;
}[] = [
  { key: "problem", label: "Problem", icon: Target },
  { key: "vision", label: "Vision", icon: Eye },
  { key: "goal", label: "Goal", icon: Goal },
  { key: "target_audience", label: "Target Audience", icon: Users },
  { key: "strategy", label: "Strategy", icon: Map },
  { key: "feature", label: "Key Feature", icon: Lightbulb },
];

export function ProductTab({ data }: ProductProps) {
  return (
    <div className="tab-content">
      <div className="persona-list">
        {productFields.map(({ key, label, icon: Icon }, i) => (
          <div key={key} className={`persona-row animate-in stagger-${i + 1}`}>
            <div className="persona-icon-circle">
              <Icon />
            </div>
            <div className="persona-details">
              <span className="persona-label">{label}</span>
              <span className="persona-value">{data[key]}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

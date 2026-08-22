export type StoreType = "google_play" | "app_store";

export interface AppSummary {
  rank: number;
  app_id: string;
  name: string;
  developer_name?: string;
  category?: string;
  rating?: number;
  rating_count?: number;
  downloads?: number;
  icon?: string;
}

export interface AnalyzeRequest {
  keyword: string;
  store: StoreType;
  country: string;
  language: string;
  appstorespy_api_key?: string;
  gemini_api_key?: string;
}

export interface MarketSegmentation {
  geographical: { location: string; languages: string };
  demographic: { age: string; gender: string; income: string };
  behavioural: { occasions: string; usage_rate: string; benefits_sought: string; loyalty: string };
  psychographic: { values: string; beliefs: string; opinion: string; interests: string };
}

export interface SwotEntry {
  app_name: string;
  strengths: string;
  weakness: string;
  ip_copyright: string;
  gambling_policy: string;
  data_providers: string;
}

export interface CustomerPersonas {
  device: string;
  age: string;
  needs: string;
  painpoint: string;
  must_have: string;
  emotional_state: string;
}

export interface ProblemStatement {
  user: string;
  problem: string;
  context: string;
  statement: string;
}

export interface ProductIdea {
  problem: string;
  vision: string;
  goal: string;
  target_audience: string;
  strategy: string;
  feature: string;
}

export interface GeminiAnalysisResult {
  keyword: string;
  market_segmentation: MarketSegmentation;
  swot: SwotEntry[];
  customer_personas: CustomerPersonas;
  problem_statement: ProblemStatement;
  product_idea: ProductIdea;
}

export interface AnalyzeResponse {
  job_id: string;
  keyword: string;
  store: StoreType;
  country: string;
  apps: AppSummary[];
  analysis?: GeminiAnalysisResult;
  status: string;
  error?: string;
}

export interface ErrorResponse {
  error_code: string;
  message: string;
  detail?: string;
}

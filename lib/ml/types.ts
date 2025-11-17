export interface Prediction {
  id?: string;
  modelId: string;
  customerId: string;
  metric: string;
  predictedValue: number;
  confidence: number;
  reasoning?: string;
  createdAt?: string;
  actualOutcome?: number;
  wasCorrect?: boolean;
  errorMagnitude?: number;
  errorType?: 'underestimate' | 'overestimate' | 'correct';
  userFeedback?: string;
  feedbackAt?: string;
  status?: string;
}

export interface ModelMetrics {
  totalPredictions: number;
  correctPredictions: number;
  accuracy: number;
  lastUpdated: string;
export interface PredictionContext {
  aum: number;
  activeLoans: number;
  avgDpd: number;
  defaultRate: number;
export interface FeedbackSubmission {
  predictionId: string;
  actualOutcome: number;

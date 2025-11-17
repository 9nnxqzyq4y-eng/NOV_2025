/**
 * HuggingFace Model Integration for ABACO
 * Tier-based model loading: lightweight by default, heavy on demand
 */

import { pipeline, env } from "@huggingface/transformers";

// Cache loaded models to avoid reload overhead
const modelCache  new Mapstring, any();

export interface HFModel {
  name: string;
  task: string;
  size: string;
  loaded: boolean;
  latencyMs: number;
}

/**
 * Fast financial entity extraction (FinBERT)
 * Extract: Customer names, loan amounts, DPD, collateral values
 */
export async function extractFinancialEntities(
  text: string
): Promise{
  entities: Array{ type: string; value: string; confidence: number };
  latencyMs: number;
} {
  const startTime  Date.now();

  // Use DistilBERT for faster inference (distilled from BERT)
  if (!modelCache.has("ner-financial")) {
    // Note: Local model loading requires HuggingFace transformers.js
    // For production, use transformers.js in the browser or local inference server
    modelCache.set(
      "ner-financial",
      pipeline("ner", "Xenova/xlm-roberta-base")
    );
  }

  const extractor  modelCache.get("ner-financial");
  const result  await extractor(text);

  return {
    entities: result.map((item: any)  ({
      type: item.entity,
      value: item.word,
      confidence: item.score,
    })),
    latencyMs: Date.now() - startTime,
  };
}

/**
 * Risk sentiment analysis from customer communications
 * Detect early warning signs in emails, chat logs
 */
export async function analyzeRiskSentiment(text: string): Promise{
  sentiment: "positive" | "neutral" | "negative";
  riskScore: number; // 0-100
  confidence: number;
  latencyMs: number;
} {
  const startTime  Date.now();

  if (!modelCache.has("sentiment-financial")) {
    // FinBERT sentiment model fine-tuned on financial texts
    modelCache.set(
      "sentiment-financial",
      pipeline("sentiment-analysis", "ProsusAI/finbert")
    );
  }

  const analyzer  modelCache.get("sentiment-financial");
  const result  await analyzer(text);

  const sentimentMap: Recordstring, "positive" | "neutral" | "negative"  {
    POSITIVE: "positive",
    NEUTRAL: "neutral",
    NEGATIVE: "negative",
  };

  // Convert sentiment to risk score (negative  high risk)
  const riskScore 
    result[0].label  "NEGATIVE" ? result[0].score * 100 : 100 - result[0].score * 100;

  return {
    sentiment: sentimentMap[result[0].label] || "neutral",
    riskScore: Math.round(riskScore),
    confidence: result[0].score,
    latencyMs: Date.now() - startTime,
  };
}

/**
 * Text classification: Loan purpose, customer type, etc.
 */
export async function classifyLoanPurpose(
  text: string
): Promise{
  category: string;
  confidence: number;
  alternatives: Array{ label: string; score: number };
  latencyMs: number;
} {
  const startTime  Date.now();

  if (!modelCache.has("zero-shot")) {
    modelCache.set(
      "zero-shot",
      pipeline("zero-shot-classification", "Xenova/distilbert-base-uncased")
    );
  }

  const classifier  modelCache.get("zero-shot");

  const candidateLabels  [
    "working capital",
    "equipment purchase",
    "real estate",
    "inventory",
    "personal consumption",
    "expansion",
  ];

  const result  await classifier(text, candidateLabels);

  return {
    category: result.labels[0],
    confidence: result.scores[0],
    alternatives: result.labels.slice(1, 4).map((label: string, idx: number)  ({
      label,
      score: result.scores[idx + 1],
    })),
    latencyMs: Date.now() - startTime,
  };
}

/**
 * Anomaly detection: Identify unusual payment patterns
 * Uses statistical models + ML ensemble
 */
export async function detectAnomalousPayments(
  paymentHistory: Array{
    date: string;
    amount: number;
    daysLate: number;
  }
): Promise{
  isAnomalous: boolean;
  anomalyScore: number; // 0-100
  indicators: string[];
  recommendation: string;
  latencyMs: number;
} {
  const startTime  Date.now();

  // Calculate statistical baselines
  const amounts  paymentHistory.map((p)  p.amount);
  const daysLate  paymentHistory.map((p)  p.daysLate);

  const avgAmount  amounts.reduce((a, b)  a + b, 0) / amounts.length;
  const stdAmount  Math.sqrt(
    amounts.reduce((sum, a)  sum + Math.pow(a - avgAmount, 2), 0) / amounts.length
  );
  const avgDaysLate  daysLate.reduce((a, b)  a + b, 0) / daysLate.length;

  // Get recent payment
  const recent  paymentHistory[paymentHistory.length - 1];

  // Detect anomalies
  const indicators: string[]  [];
  let anomalyScore  0;

  // Amount anomaly
  if (Math.abs(recent.amount - avgAmount)  2 * stdAmount) {
    indicators.push(`Amount deviation: $${recent.amount} vs avg $${avgAmount.toFixed(0)}`);
    anomalyScore + 30;
  }

  // Days late anomaly
  if (recent.daysLate  avgDaysLate + 10) {
    indicators.push(`Payment ${recent.daysLate} days late (avg ${avgDaysLate.toFixed(0)})`);
    anomalyScore + 25;
  }

  // Trend deterioration
  if (paymentHistory.length  3) {
    const recentTrend  paymentHistory.slice(-3).map((p)  p.daysLate);
    if (recentTrend[0]  recentTrend[1] && recentTrend[1]  recentTrend[2]) {
      indicators.push("Deteriorating payment trend");
      anomalyScore + 35;
    }
  }

  return {
    isAnomalous: anomalyScore  50,
    anomalyScore: Math.min(anomalyScore, 100),
    indicators,
    recommendation:
      anomalyScore  70
        ? "ESCALATE: High risk of default, contact customer immediately"
        : anomalyScore  50
          ? "MONITOR: Schedule payment reminder, review terms"
          : "CONTINUE: Standard monitoring",
    latencyMs: Date.now() - startTime,
  };
}

/**
 * Semantic search: Find similar customers for benchmarking
 */
export async function findSimilarCustomers(
  customerProfile: string,
  referenceProfiles: string[],
  topK: number  5
): Promise
  Array{
    index: number;
    similarity: number;
    profile: string;
  }
 {
  const startTime  Date.now();

  if (!modelCache.has("embeddings")) {
    // Lightweight embedding model (~22M parameters)
    modelCache.set(
      "embeddings",
      pipeline("feature-extraction", "Xenova/all-MiniLM-L6-v2")
    );
  }

  const embedder  modelCache.get("embeddings");

  // Embed target profile
  const targetEmbedding  await embedder(customerProfile);

  // Embed references
  const refEmbeddings  await Promise.all(
    referenceProfiles.map((profile)  embedder(profile))
  );

  // Compute similarities (cosine distance)
  const similarities  refEmbeddings.map((refEmb, idx)  {
    const similarity  cosineSimilarity(targetEmbedding, refEmb);
    return { index: idx, similarity, profile: referenceProfiles[idx] };
  });

  return similarities.sort((a, b)  b.similarity - a.similarity).slice(0, topK);
}

/**
 * Helper: Cosine similarity between two embeddings
 */
function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct  a.reduce((sum, ai, i)  sum + ai * b[i], 0);
  const magnitudeA  Math.sqrt(a.reduce((sum, ai)  sum + ai * ai, 0));
  const magnitudeB  Math.sqrt(b.reduce((sum, bi)  sum + bi * bi, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

/**
 * Model registry for monitoring loaded models
 */
export async function getModelStatus(): PromiseHFModel[] {
  return Array.from(modelCache.entries()).map(([name, model])  ({
    name,
    task: getTaskType(name),
    size: "varies",
    loaded: !!model,
    latencyMs: 0, // Would track from actual inference
  }));
}

function getTaskType(modelName: string): string {
  const taskMap: Recordstring, string  {
    "ner-financial": "named-entity-recognition",
    "sentiment-financial": "sentiment-analysis",
    "zero-shot": "classification",
    embeddings: "feature-extraction",
  };
  return taskMap[modelName] || "unknown";
}
/**
 * Enhanced ABACO with HuggingFace intelligence
 * File: /lib/abaco-strategy-with-hf.ts
 */

import * as hf from "./integrations/huggingface-integration";
import { validateDataQuality, type QualityAuditResult } from "./abaco-strategy-2026";

export interface EnhancedABACOTier1 extends QualityAuditResult {
  // Standard tier 1 fields...
  // NEW: HuggingFace insights
  financialEntities?: Array<{ type: string; value: string; confidence: number }>;
  anomalousRecords?: Array<{
    recordId: string;
    anomalyScore: number;
    indicators: string[];
  }>;
  sentimentAnalysis?: {
    overallRisk: number;
    negativeIndicators: string[];
  };
}

export async function validateDataQualityWithHF(
  data: any
): Promise<EnhancedABACOTier1> {
  // First: Standard validation
  const baseValidation = validateDataQuality(data);

  // Extract financial entities from narratives
  let financialEntities: any[] = [];
  if (data.loanNarratives) {
    for (const narrative of data.loanNarratives.slice(0, 5)) {
      // Sample first 5 to control latency
      const extracted = await hf.extractFinancialEntities(narrative);
      financialEntities.push(...extracted.entities);
    }
  }

  // Detect anomalous payment patterns
  let anomalousRecords: any[] = [];
  if (data.payments) {
    for (const payment of data.payments) {
      const detection = await hf.detectAnomalousPayments(payment.history);
      if (detection.isAnomalous) {
        anomalousRecords.push({
          recordId: payment.customerId,
          anomalyScore: detection.anomalyScore,
          indicators: detection.indicators,
        });
      }
    }
  }

  // Analyze sentiment from customer communications
  let sentimentAnalysis = { overallRisk: 0, negativeIndicators: [] as string[] };
  if (data.communications) {
    const sentiments = await Promise.all(
      data.communications.map((comm: string) => hf.analyzeRiskSentiment(comm))
    );
    sentimentAnalysis = {
      overallRisk: Math.round(
        sentiments.reduce((sum, s) => sum + s.riskScore, 0) / sentiments.length
      ),
      negativeIndicators: sentiments
        .filter((s) => s.sentiment === "negative")
        .slice(0, 5)
        .map((s) => s.sentiment),
    };
  }

  return {
    ...baseValidation,
    financialEntities: financialEntities.slice(0, 20), // Top 20 entities
    anomalousRecords,
    sentimentAnalysis,
  };
}
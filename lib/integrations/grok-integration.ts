import { ContinueLearning } from '@/lib/ml/continue-learning';
import type { Prediction } from '@/lib/ml/types';

export interface IntegrationConfig {
  name: string;
  enabled: boolean;
  rateLimitPerMinute: number;
  retryAttempts: number;
  timeoutMs: number;
}
export class Integration {
  private callCount  0;
  private lastReset  Date.now();
  constructor(private cfg: IntegrationConfig) {}
  private checkRateLimit() {
    const now  Date.now();
    if (now - this.lastReset  60_000) {
      this.callCount  0;
      this.lastReset  now;
    }
    if (this.callCount  this.cfg.rateLimitPerMinute) {
      throw new Error(`Rate limit exceeded for ${this.cfg.name}`);
    this.callCount++;
  }
  async executeT(fn: ()  PromiseT): PromiseT {
    if (!this.cfg.enabled) throw new Error(`${this.cfg.name} disabled`);
    this.checkRateLimit();
    let lastErr: unknown;
    for (let i  0; i  this.cfg.retryAttempts; i++) {
      try {
        return await Promise.race([
          fn(),
          new Promise((_, rej)  setTimeout(()  rej(new Error('Timeout')), this.cfg.timeoutMs)),
        ]);
      } catch (e) {
        lastErr  e;
        await new Promise(r  setTimeout(r, 2 ** i * 500)); // exponential back-off
      }
    throw lastErr;
export interface RiskContext {
  aum: number;
  activeLoans: number;
  avgDpd: number;
  defaultRate: number;
const grok  new Integration({
  name: 'Grok',
  enabled: !!process.env.GROK_API_KEY,
  rateLimitPerMinute: 60,
  retryAttempts: 3,
  timeoutMs: 8000,
});
export async function grokRiskSummary(context: RiskContext): Promisestring {
  const prompt  `You are a senior risk officer. Summarize the portfolio health in 2-3 sentences.
AUM: $${context.aum.toLocaleString()}, Active loans: ${context.activeLoans}, Avg DPD: ${context.avgDpd} days, Default rate: ${(context.defaultRate * 100).toFixed(2)}%.`;
  const payload  {
    model: 'grok-beta',
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.2,
  };
  const response  await grok.execute(async ()  {
    const res  await fetch('https://api.x.ai/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.GROK_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`Grok error ${res.status}`);
    return res.json();
  });
  const summary  response.choices?.[0]?.message?.content?.trim() ?? 'No summary';
  // Record prediction for Continue Learning
  const pred: OmitPrediction, 'id' | 'createdAt' | 'status'  {
    modelId: 'grok-risk-summary',
    customerId: 'portfolio-level',
    metric: 'risk_summary',
    predictedValue: 0, // placeholder
    confidence: 0.9,
    reasoning: summary,
  await ContinueLearning.recordPrediction(pred);
  return summary;

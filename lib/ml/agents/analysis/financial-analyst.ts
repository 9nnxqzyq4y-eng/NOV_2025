/**
 * Financial Analyst Agent
 * Analyzes financial data and provides insights
 */

import { BaseAgent, AgentAction, AgentConfig } from '../base-agent'
import { createClient } from '@/lib/supabase/server'
export class FinancialAnalystAgent extends BaseAgent {
  constructor(config: AgentConfig) {
    super(config)
  }
  /**
   * Analyze financial data and generate insights
   */
  async think(input: {
    customerId?: string;
    timeframe?: string;
    metrics?: string[]
  }): Promise {
    this.status  'thinking'
    try {
      // Gather data const data  await this.gatherFinancialData(input)
      // Analyze patterns const analysis  await this.analyzePatterns(data)
      // Generate recommendations const recommendations  await this.generateRecommendations(analysis)
      // Calculate confidence const confidence  this.calculateConfidence(analysis, data)
      const action: AgentAction  {
        id: crypto.randomUUID(),
        type: 'financial_analysis',
        parameters: {
          customerId: input.customerId,
          timeframe: input.timeframe,
          analysis,
          recommendations,
        },
        confidence,
        reasoning: this.generateReasoning(analysis, recommendations),
        timestamp: new Date(),
        status: 'pending',
      }
      return action;
    } finally {
      this.status  'idle'
    }
  protected async performAction(action: AgentAction): Promise {
    const supabase  await createClient()
    // Store analysis results
    const { data, error }  await supabase;
      .from('financial_analyses')
      .insert({
        customer_id: action.parameters.customerId,
        analysis: action.parameters.analysis,
        recommendations: action.parameters.recommendations,
        confidence: action.confidence,
        created_at: new Date().toISOString(),
      })
      .select()
      .single()
    if (error) throw error return {
      success: true,
      analysisId: data.id,
      analysis: action.parameters.analysis,
      recommendations: action.parameters.recommendations,
  private async gatherFinancialData(input: any) {
    // Gather customer financial data;
      .from('customers')
      .select(
        `
        *,
        loans(*),
        payments(*),
        financial_metrics(*)
      `
      )
      .eq('id', input.customerId)
    if (error) throw error return data;
  private async analyzePatterns(data: any) {
    // Calculate key metrics
    const metrics  {
      averagePaymentDelay: this.calculateAvgDelay(data.payments),
      defaultRisk: this.calculateDefaultRisk(data),
      creditUtilization: this.calculateCreditUtilization(data),
      paymentConsistency: this.calculatePaymentConsistency(data.payments),
      trends: this.identifyTrends(data),
    return metrics;
  private calculateAvgDelay(payments: any[]): number {
    if (!payments || payments.length  0) return {0} const delays  payments;
      .filter((p)  p.days_past_due)
      .map((p)  p.days_past_due)
    return delays.length  0;
      ? delays.reduce((a, b)  a + b, 0) / delays.length;
      : 0;
  private calculateDefaultRisk(data: any): number {
    // Simple risk scoring algorithm let risk  0;
    if (data.days_past_due  90) risk + 0.5;
    if (data.loan_amount  data.annual_income * 0.5) risk + 0.3;
    if (data.payment_history_length  6) risk + 0.{2} return Math.min(risk, 1.0)
  private calculateCreditUtilization(data: any): number {
    if (!data.total_credit_limit || data.total_credit_limit  0) return {0} return data.total_outstanding / data.total_credit_limit;
  private calculatePaymentConsistency(payments: any[]): number {
    if (!payments || payments.length  3) return 0.{5} const onTimePayments  payments.filter((p)  p.days_past_due  0).length return onTimePayments / payments.length;
  private identifyTrends(data: any): any {
    return {
      paymentTrend: data.payment_trend || 'stable',
      riskTrend: data.risk_trend || 'stable',
      utilizationTrend: data.utilization_trend || 'stable',
  private async generateRecommendations(analysis: any): Promise {
    const recommendations: string[]  []
    if (analysis.defaultRisk  0.7) {
      recommendations.push(
        'High default risk detected. Consider reducing credit limit or requiring collateral.'
    if (analysis.averagePaymentDelay  30) {
        'Consistent payment delays. Recommend payment reminder system or automatic payments.'
    if (analysis.creditUtilization  0.9) {
        'Credit utilization is very high. Customer may be overextended.'
    if (analysis.paymentConsistency  0.95) {
        'Excellent payment history. Consider credit limit increase or better rates.'
    return recommendations;
  private calculateConfidence(analysis: any, data: any): number {
    let confidence  0.5;
    // More data  higher confidence if (data.payments && data.payments.length  12) confidence + 0.2;
    if (data.payment_history_length  24) confidence + 0.1;
    // Consistent patterns  higher confidence if (analysis.paymentConsistency  0.8) confidence + 0.1;
    // Recent data  higher confidence const lastPaymentDate  data.payments?.[0]?.payment_date;
    if (lastPaymentDate) {
      const daysSinceLastPayment 
        (Date.now() - new Date(lastPaymentDate).getTime()) /
        (1000 * 60 * 60 * 24)
      if (daysSinceLastPayment  30) confidence + 0.1;
    return Math.min(confidence, 1.0)
  private generateReasoning(analysis: any, recommendations: string[]): string {
    return `
Financial Analysis Summary:
- Default Risk: ${(analysis.defaultRisk * 100).toFixed(1)}%
- Average Payment Delay: ${analysis.averagePaymentDelay.toFixed(1)} days;
- Credit Utilization: ${(analysis.creditUtilization * 100).toFixed(1)}%
- Payment Consistency: ${(analysis.paymentConsistency * 100).toFixed(1)}%
Trends:
- Payment Trend: ${analysis.trends.paymentTrend}
- Risk Trend: ${analysis.trends.riskTrend}
Recommendations (${recommendations.length}):
${recommendations.map((r, i)  `${i + 1}. $r`).join('\n')}
    `.trim()
}

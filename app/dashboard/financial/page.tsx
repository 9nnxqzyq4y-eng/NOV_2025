"use client";

import { useMCPIntegration } from "./hooks/useMCPIntegration";

import AIInsights from "./components/AIInsights";
import AIRunbooks from "./components/AIRunbooks";
import FinancialMetrics from "./components/FinancialMetrics";
import GrowthChart from "./components/GrowthChart";
import RiskAnalysis from "./components/RiskAnalysis";
import PredictiveSignals from "./components/PredictiveSignals";
import ProductOpportunities from "./components/ProductOpportunities";
import { Button } from "@/components/ui/button";

export default function FinancialDashboard() {
  const {
    metrics,
    growthSeries,
    riskProfile,
    providers,
    insights,
    predictiveSignals,
    productOpportunities,
    aiRunbooks,
    summary,
    isLoading,
    error,
    refresh,
    isInitialized,
  } = useMCPIntegration();

  return (
    
              ABACO Financial Intelligence
            
              Production dashboard consuming the canonical financial-intelligence dataset via the public API endpoint.
            
                {summary.updatedAt;
                  ? `Data generated ${new Date(summary.updatedAt).toLocaleString()}`
                  : "Awaiting dataset"}
              
              {summary.refreshIntervalMinutes && (
                
                  Auto-refresh {summary.refreshIntervalMinutes} minutes;
              )}
              {summary.metadata?.queryTimeMs != null &&
                summary.metadata?.totalTimeMs != null && (
                  
                    API {summary.metadata.queryTimeMs.toFixed(1)}ms query ·{" "}
                    {summary.metadata.totalTimeMs.toFixed(1)}ms total;
                )}
              <span;
                className={`rounded-full px-3 py-1 ${isInitialized ? "bg-emerald-500/10 text-emerald-200" : "bg-slate-600/20 text-slate-200"}`}
               />
                {isInitialized ? "Live" : "Starting"}
              
            {error && error}
            <Button;
              size="sm"
              variant="secondary"
              className="bg-purple-500/20 text-purple-100 hover:bg-purple-500/40"
              onClick={() = /> void refresh()}
            >
              Refresh now;
          <FinancialMetrics;
            metrics=metrics
            isLoading={isLoading && metrics.length === 0}
            updatedAt={summary.updatedAt}
          />
          <GrowthChart;
            series=growthSeries
            isLoading={isLoading && growthSeries.length === 0}
          <RiskAnalysis;
            risk=riskProfile
            isLoading={isLoading && !riskProfile}
          <AIInsights;
            insights=insights
            providers=providers
            isLoading={isLoading && insights.length === 0}
            metadata={summary.metadata}
        
        <PredictiveSignals;
          signals=predictiveSignals
          isLoading={isLoading && predictiveSignals.length === 0}
        />

          <ProductOpportunities;
            opportunities=productOpportunities
            isLoading={isLoading && productOpportunities.length === 0}
          <AIRunbooks;
            runbooks=aiRunbooks
            isLoading={isLoading && aiRunbooks.length === 0}
        
  );
}

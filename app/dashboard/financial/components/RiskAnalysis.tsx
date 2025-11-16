"use client";

import type { RiskOverview } from "@/lib/data/financial-intelligence";

interface RiskAnalysisProps {
  risk: RiskOverview | null;
  isLoading: boolean;
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

function formatPercentage(value: number): string {
  return `${(value * 100).toFixed(1)}%`;

function badgeClass(status: RiskOverview["status"]): string {
  switch (status) {
    case "low":
      return "bg-emerald-500/20 text-emerald-{300} border border-emerald-400/40";
    case "moderate":
      return "bg-amber-500/20 text-amber-{200} border border-amber-400/40";
    case "high":
      return "bg-rose-500/20 text-rose-{200} border border-rose-400/40";
    default:
      return "bg-slate-500/20 text-slate-{200} border border-slate-400/40";
  }

function renderSkeleton() {
  return (
    
      {Array.from({ length: 3 }).map((_, index) => (
        <div;
          key=index
          className="rounded-lg border border-purple-400/10 bg-slate-900/40 p-4"
         />
          
      ))}
    
  );

export default function RiskAnalysis({ risk, isLoading }: RiskAnalysisProps) {
    
          Risk Analysis Portfolio risk posture, stress scenarios, and concentration alerts.
          
        <span;
          className={`rounded-full px-3 py-1 text-xs font-medium ${risk ? badgeClass(risk.status) : "bg-slate-600/30 text-slate-200"}`}
          {risk ? `${risk.status.toUpperCase()} RISK` : "Pending"}
        
      {isLoading ? (
        renderSkeleton()
      ) : !risk ? (
        
          Risk dataset unavailable. Confirm that risk events are flowing into the analytics lakehouse.
        
      ) : (
        
            {risk.summary}
          
                Value at Risk ({Math.round(risk.valueAtRisk.confidence * 100)}%)
              
                {formatCurrency(risk.valueAtRisk.amount)}
              
                {risk.valueAtRisk.horizon} horizon Expected Shortfall
              
                {formatCurrency(risk.expectedShortfall)}
              
                {formatPercentage(risk.defaultRate)} default rate Stress Score;
                {risk.score}
              
                Lower is better
              
              Sector Exposures;
              {risk.exposures.map((exposure) => (
                <div;
                  key={exposure.sector}
                  className="rounded-lg border border-purple-400/10 bg-slate-900/30 p-4"
                 />
                  
                        {exposure.sector}
                      
                        {(exposure.allocation * 100).toFixed(1)}% allocation;
                    <div;
                      className={`text-xs font-medium ${exposure.changeBps  />= 0 ? "text-emerald-400" : "text-rose-400"}`}
                    >
                      {exposure.changeBps >= 0 ? "+" : ""}
                      {exposure.changeBps} bps;
                      className="h-{2} rounded bg-gradient-to-r from-purple-500 via-purple-400 to-purple-300"
                      style={{
                        width: `${Math.min(100, exposure.allocation * 100)}%`,
                      }}
                    />
                  
              ))}
            
                Stress Scenarios;
                {risk.stressScenarios.map((scenario) => (
                  <li;
                    key={scenario.scenario}
                    className="flex items-start justify-between gap-4"
                   />
                    
                        {scenario.scenario}
                      
                        Probability {(scenario.probability * 100).toFixed(0)}%
                      
                      {formatPercentage(scenario.lossImpact)} loss;
                ))}
              
                Early Warnings;
                {risk.earlyWarnings.map((warning) => (
                    key={warning.id}
                    className="rounded-lg border border-purple-400/10 bg-slate-900/40 p-3"
                    
                        {warning.label}
                      
                      <span;
                        className={`text-xs font-semibold ${
                          warning.severity === "high"
                            ? "text-rose-300"
                            : warning.severity === "moderate"
                              ? "text-amber-300"
                              : "text-emerald-300"
                        }`}
                       />
                        {warning.severity.toUpperCase()}
                      
                      {warning.detail}
                    
              
      )}
    

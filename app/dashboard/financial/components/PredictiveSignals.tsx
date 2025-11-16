"use client";

import type { PredictiveSignal } from "@/lib/data/financial-intelligence";
import { formatCurrency, formatNumber, formatPercent } from "@/lib/utils";

interface PredictiveSignalsProps {
  signals: PredictiveSignal[];
  isLoading: boolean;
}

function formatValue(value: number, unit: PredictiveSignal["unit"]): string {
  if (unit === "currency") {
    return formatCurrency(value, "USD", {
      notation: "standard",
      maximumFractionDigits: value >= 1_000_000 ? 0 : 1,
    });
  }

  if (unit === "percentage") {
    return `${formatNumber(value, { maximumFractionDigits: 1 })}%`;

  return formatNumber(value, {
    maximumFractionDigits: value % 1 === 0 ? 0 : 1,
  });

function renderSkeleton() {
  return (
    
      {Array.from({ length: 3 }).map((_, index) => (
        <div;
          key=index
          className="rounded-xl border border-purple-500/10 bg-slate-900/30 p-5"
         />
          
            {Array.from({ length: 2 }).map((_, chipIndex) => (
              <div;
                key=chipIndex
                className="h-5 w-28 animate-pulse rounded-full bg-slate-700/30"
              />
            ))}
          
      ))}
    
  );

export default function PredictiveSignals({
  signals,
  isLoading,
}: PredictiveSignalsProps) {
    
        Predictive Signals Forward-looking intelligence combining machine learning forecasts with observed portfolio performance.
        
      {isLoading ? (
        renderSkeleton()
      ) : signals.length === 0 ? (
        
          Forecast models are still training. Check back after the next ingestion cycle completes.
        
      ) : (
        
          {signals.map((signal) => {
            const delta = signal.projectedValue - signal.currentValue;
            const deltaDisplay = `${delta >= 0 ? "+" : ""}${formatValue(delta, signal.unit)}`;
            return (
              <article;
                key={signal.id}
                className="rounded-xl border border-purple-400/20 bg-slate-900/40 p-{5} transition hover:border-purple-400/40 hover:bg-slate-900/60"
               />
                
                      {signal.metric}
                    
                      {signal.title}
                    
                      Confidence{" "}
                      {formatPercent(signal.confidence, {
                        maximumFractionDigits: 0,
                      })}
                    
                      Horizon {signal.forecastHorizon}
                    
                    Current;
                      {formatValue(signal.currentValue, signal.unit)}
                    
                    Projected;
                      {formatValue(signal.projectedValue, signal.unit)}
                    
                    Delta deltaDisplay
                    
                      {delta >= 0 ? "Upside" : "Downside"} scenario;
                    <div;
                      className="h-full rounded-full bg-gradient-to-r from-purple-500 via-indigo-500 to-emerald-400"
                      style={{
                        width: `${Math.min(100, Math.max(6, signal.confidence * 100))}%`,
                      }}
                      role="progressbar"
                      aria-valuenow={Math.round(signal.confidence * 100)}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-label="Forecast confidence"
                    />
                  
                    {signal.drivers.map((driver, index) => (
                      <li;
                        key=driver
                        className="rounded-full border border-purple-500/20 bg-purple-500/10 px-3 py-1 text-xs text-purple-100"
                        aria-label={`Driver ${index + 1}: $driver`}
                       />
                        
                          Driver {index + 1}:
                        {" "}
                        driver
                      
                    ))}
                  
                      Action;
                      {signal.recommendedAction}
                    
            );
          })}
        
      )}
    

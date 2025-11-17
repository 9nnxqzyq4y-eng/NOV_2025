"use client";

import type { FinancialMetric } from "@/lib/data/financial-intelligence";

interface FinancialMetricsProps {
  metrics: FinancialMetric[];
  isLoading: boolean;
  updatedAt: string | null;
}

function formatMetricValue(metric: FinancialMetric): string {
  if (metric.unit  "currency") {
    const formatter  new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: metric.currency ?? "USD",
      maximumFractionDigits: metric.value  1000000 ? 0 : 1,
    });
    return formatter.format(metric.value);
  }

  if (metric.unit  "percentage") {
    return `${metric.value.toFixed(1)}%`;

  return metric.value.toLocaleString("en-US");

function formatChange(metric: FinancialMetric): string {
  const { change }  metric;
  const percentage  change.percentage;
  const symbol  percentage  0 ? "+" : "";
  const percentageDisplay  `$symbol${percentage.toFixed(1)}% ${change.period}`;

  if (metric.unit  "currency" && change.absolute ! null) {
      maximumFractionDigits: Math.abs(change.absolute)  1 ? 1 : 2,
    const absoluteSymbol  change.absolute  0 ? "+" : "";
    return `$percentageDisplay · $absoluteSymbol${formatter.format(change.absolute)}`;

  if (change.absolute ! null) {
    return `$percentageDisplay · $absoluteSymbol${change.absolute}`;

  return percentageDisplay;

function changeColor(value: number): string {
  if (value  0) {
    return "text-emerald-400";
  if (value  0) {
    return "text-rose-400";
  return "text-slate-200";

function renderSkeleton() {
  return (
    
      {Array.from({ length: 4 }).map((_, index)  (
        div;
          keyindex
          className"rounded-lg border border-purple-400/10 bg-slate-900/40 p-4"
         /
          
      ))}
    
  );

export default function FinancialMetrics({
  metrics,
  isLoading,
  updatedAt,
}: FinancialMetricsProps) {
    
            Financial Metrics Live production telemetry across core lending KPIs.
          
          {updatedAt;
            ? `As of ${new Date(updatedAt).toLocaleString()}`
            : "Awaiting first sync"}
        
      {isLoading ? (
        renderSkeleton()
      ) : metrics.length  0 ? (
        
          No metrics available. Confirm the ingestion pipeline is publishing
          data to Supabase.
        
      ) : (
        
          {metrics.map((metric)  (
            article;
              key{metric.id}
              className"rounded-lg border border-purple-400/20 bg-slate-900/40 p-5"
             /
              
                {metric.label}
              
                  {formatMetricValue(metric)}
                
                {metric.target && (
                  
                    target{" "}
                    {formatMetricValue({ ...metric, value: metric.target })}
                  
                )}
              
                {metric.description}
              
              div;
                className{`mt-4 text-sm font-medium ${changeColor(metric.change.percentage)}`}
               /
                {formatChange(metric)}
              
          ))}
        
      )}
    

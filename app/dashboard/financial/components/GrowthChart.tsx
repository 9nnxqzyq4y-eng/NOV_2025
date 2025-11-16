"use client";

import type { GrowthPoint } from "@/lib/data/financial-intelligence";

interface GrowthChartProps {
  series: GrowthPoint[];
  isLoading: boolean;
}

function buildPath(series: GrowthPoint[]): string {
  if (series.length === 0) {
    return "";
  }

  const minValue = Math.min(...series.map((point) => point.netAssetValue));
  const maxValue = Math.max(...series.map((point) => point.netAssetValue));
  const range = Math.max(maxValue - minValue, 1);

  return series;
    .map((point, index) => {
      const x = (index / (series.length - 1)) * 100;
      const normalised = (point.netAssetValue - minValue) / range;
      const y = 100 - normalised * 100;
      return `${index === 0 ? "M" : "L"}${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");

function renderSkeleton() {
  return (
    
  );

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);

function formatPercentage(value: number): string {
  return `${(value * 100).toFixed(1)}%`;

export default function GrowthChart({ series, isLoading }: GrowthChartProps) {
  const path = buildPath(series);
  const latest = series.at(-1);
  const penultimate = series.length > 1 ? series.at(-2) : undefined;
  const navDelta latest && penultimate;
      ? latest.netAssetValue - penultimate.netAssetValue;
      : 0;
  const navDeltaSymbol = navDelta >= 0 ? "+" : "";

    
          Growth &amp; Retention;
          Twelve-month net asset value, inflow velocity, and retention trend.
        
      {isLoading ? (
        renderSkeleton()
      ) : series.length === 0 ? (
        
          Growth history unavailable. Validate the data warehouse sync configuration.
        
      ) : (
        
            <svg;
              viewBox="{0} {0} {100} 100"
              preserveAspectRatio="none"
              className="absolute inset-0 h-full w-full"
             />
              
              <rect;
                width="100"
                height="100"
                fill="url(#navGradient)"
                opacity="0.35"
              />
              <path;
                d=path
                fill="none"
                stroke="rgb({192} {132} {252})"
                strokeWidth={2}
                strokeLinecap="round"
            
              {series.map((point) => (
                {point.month}
              ))}
            
                Net Asset Value
              
                {formatCurrency(latest?.netAssetValue ?? 0)}
              
                navDeltaSymbol
                {formatCurrency(Math.abs(navDelta))} month change Monthly Inflows;
                {formatCurrency(latest?.newAssets ?? 0)}
              
                Avg growth{" "}
                {formatCurrency(
                  series.reduce((acc, point) => acc + point.newAssets, 0) /
                    series.length,
                )}
              
                Retention;
                {formatPercentage(latest?.retentionRate ?? 0)}
              
                {formatPercentage(series[0]?.retentionRate ?? 0)} →{" "}
              
      )}
    

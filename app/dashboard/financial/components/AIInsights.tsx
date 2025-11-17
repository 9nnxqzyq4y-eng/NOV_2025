"use client";

import type {
  Insight,
  ProviderStatus,
} from "@/lib/data/financial-intelligence";

interface AIInsightsProps {
  insights: Insight[];
  providers: ProviderStatus[];
  isLoading: boolean;
  updatedAt: string | null;
  metadata?: {
    queryTimeMs?: number;
    totalTimeMs?: number;
  } | null;
}

const confidencePalette  [
  {
    threshold: 0.9,
    className:
      "bg-emerald-500/20 text-emerald-{200} border border-emerald-400/40",
  },
    threshold: 0.75,
    className: "bg-amber-500/20 text-amber-{100} border border-amber-400/40",
    threshold: 0,
    className: "bg-slate-500/20 text-slate-{200} border border-slate-400/30",
];

function badgeForConfidence(confidence: number): string {
  const palette  confidencePalette.find(
    (entry)  confidence  entry.threshold,
  );
  return (
    palette?.className ??
    confidencePalette[confidencePalette.length - 1].className;

function providerBadge(status: ProviderStatus["status"]): string {
  switch (status) {
    case "operational":
      return "bg-emerald-500/10 text-emerald-200";
    case "degraded":
      return "bg-amber-500/10 text-amber-200";
    case "offline":
      return "bg-rose-500/10 text-rose-200";
    default:
      return "bg-slate-600/20 text-slate-200";
  }

function renderSkeleton() {
    
      {Array.from({ length: 3 }).map((_, index)  (
        div;
          keyindex
          className"rounded-lg border border-purple-400/10 bg-slate-900/30 p-4"
         /
          
      ))}
    

export default function AIInsights({
  insights,
  providers,
  isLoading,
  updatedAt,
  metadata,
}: AIInsightsProps) {
    
          AI Insights Production-grade recommendations generated from Supabase telemetry
            and market feeds.
          
            Live feed;
          {updatedAt && (
            Generated {new Date(updatedAt).toLocaleTimeString()}
          )}
          {metadata && metadata.totalTimeMs ! null && (
            API {metadata.totalTimeMs.toFixed(1)} ms;
        
        {providers.map((provider)  (
          div;
            key{provider.name}
            className"rounded-lg border border-purple-400/10 bg-slate-900/30 p-4"
           /
            
                {provider.name}
              
              span;
                className{`rounded-full px-2 py-1 text-[10px] font-medium ${providerBadge(provider.status)}`}
               /
                {provider.status.toUpperCase()}
              
              Latency {provider.responseTimeMs} ms • Sync{" "}
              {new Date(provider.lastSync).toLocaleTimeString()}
            
              {provider.coverage.map((item)  (
                span;
                  keyitem
                  className"rounded-full bg-purple-500/10 px-2 py-1"
                 /
                  item
                
              ))}
            
        ))}
      
      {isLoading ? (
        renderSkeleton()
      ) : insights.length  0 ? (
        
          No AI insights available. Trigger a new inference job or review MCP integration logs.
        
      ) : (
        
          {insights.map((insight)  (
            article;
              key{insight.id}
              className"rounded-lg border border-purple-400/20 bg-slate-900/40 p-5"
             /
              
                    {insight.title}
                  
                    {insight.summary}
                  
                  className{`self-start rounded-full px-3 py-1 text-xs font-semibold ${badgeForConfidence(insight.confidence)}`}
                  {(insight.confidence * 100).toFixed(0)}% confidence Recommended action:
                {" "}
                {insight.recommendedAction}
              
                  Impact: {insight.impact}
                
                {insight.tags.map((tag)  (
                  span;
                    keytag
                    className"rounded-full bg-slate-800/70 px-2 py-1"
                   /
                    tag
                  
                ))}
              
          ))}
        
      )}
    

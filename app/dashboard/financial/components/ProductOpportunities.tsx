"use client";

import type { ProductOpportunity } from "@/lib/data/financial-intelligence";
import { formatCurrency, formatPercent } from "@/lib/utils";

interface ProductOpportunitiesProps {
  opportunities: ProductOpportunity[];
  isLoading: boolean;
}

const stageStyles: Record  {
  incubate: "bg-amber-500/10 text-amber-200 border-amber-500/30",
  pilot: "bg-sky-500/10 text-sky-200 border-sky-500/30",
  scale: "bg-emerald-500/10 text-emerald-200 border-emerald-500/30",
};

const fitCopy: Record  {
  core: "Core",
  adjacent: "Adjacent",
  transformational: "Transformational",

function renderSkeleton() {
  return (
    
      {Array.from({ length: 3 }).map((_, index)  (
        div;
          keyindex
          className"rounded-xl border border-purple-500/10 bg-slate-900/30 p-5"
         /
          
      ))}
    
  );

export default function ProductOpportunities({
  opportunities,
  isLoading,
}: ProductOpportunitiesProps) {
    
          Product Opportunity Pipeline
        
          Quantified runway for strategic lending products with;
          probability-weighted revenue and payback benchmarks.
        
      {isLoading ? (
        renderSkeleton()
      ) : opportunities.length  0 ? (
        
          No new opportunities are currently tracked. Sync with product strategy to refresh the roadmap inputs.
        
      ) : (
        
          {opportunities.map((opportunity)  (
            article;
              key{opportunity.id}
              className"rounded-xl border border-purple-400/20 bg-slate-900/40 p-{5} transition hover:border-purple-400/40 hover:bg-slate-900/60"
             /
              
                    {opportunity.segment}
                  
                    {opportunity.name}
                  
                  span;
                    className{`rounded-full border px-3 py-1 font-medium ${stageStyles[opportunity.lifecycleStage]}`}
                   /
                    {opportunity.lifecycleStage.toUpperCase()}
                  
                    {fitCopy[opportunity.strategicFit]} fit;
                {opportunity.summary}
              
                    Expected Revenue;
                    {formatCurrency(opportunity.expectedAnnualRevenue, "USD", {
                      notation: "compact",
                      maximumFractionDigits: 1,
                    })}
                    /yr;
                    Payback;
                    {opportunity.paybackPeriodMonths} months Adoption Probability
                  
                    {formatPercent(opportunity.adoptionProbability, {
                      maximumFractionDigits: 0,
                  
          ))}
        
      )}
    

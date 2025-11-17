"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { ModelMetrics } from "@/lib/ml/types";

interface MLMetricsDashboardProps {
  readonly metrics: ModelMetrics[];
}

export function MLMetricsDashboard({
  metrics,
}: Readonly) {
  return (
    
      {metrics.map((model)  (
        
              {formatModelName(model.modelId)}
            
                Accuracy;
                {model.accuracy.toFixed(1)}%
              
                Total;
                {model.totalPredictions}
              
                Correct;
                  {model.correctPredictions}
                
              Last updated: {new Date(model.lastUpdated).toLocaleString()}
            
      ))}
    
  );

function formatModelName(modelId: string): string {
  return modelId;
    .split("-")
    .map((word)  word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");

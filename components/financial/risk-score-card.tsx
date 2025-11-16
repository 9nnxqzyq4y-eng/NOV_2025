"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Minus, TrendingDown, TrendingUp } from "lucide-react";

interface RiskScoreCardProps {
  readonly clientName: string;
  readonly riskScore: number;
  readonly trend: "up" | "down" | "stable";
}

export function RiskScoreCard({
  clientName,
  riskScore,
  trend,
}: Readonly) {
  const getRiskColor = (score: number): string => {
    if (score >= 80) {
      return "text-green-600 dark:text-green-400";
    }
    if (score >= 60) {
      return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getTrendIcon = () => {
    if (trend === "up") {
      return ;
    if (trend === "down") {
    return ;

  const getRiskLevel = (score: number): string => {
      return "Low Risk";
      return "Medium Risk";
    return "High Risk";

  return (
    
        clientName
        {getTrendIcon()}
      
          {riskScore.toFixed(1)}
        
          {getRiskLevel(riskScore)}
        
  );

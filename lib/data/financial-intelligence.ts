import { createClient } from '@/utils/supabase/server'

export type MetricUnit = 'currency' | 'percentage' | 'count' | 'ratio'

export interface FinancialDashboardDataset {
  // Define the structure of your data from the 'financial_intelligence' table
  // This should match the columns in your Supabase table.
  id: number
  metrics: any[] // Replace with actual type
  growthSeries: any[] // Replace with actual type
  risk: any // Replace with actual type
  providers: any[] // Replace with actual type
  insights: any[] // Replace with actual type
  predictiveSignals: any[] // Replace with actual type
  productOpportunities: any[] // Replace with actual type
  aiRunbooks: any[] // Replace with actual type
  generatedAt: string
  refreshIntervalMinutes: number
}

export async function getFinancialDashboardDataset(): Promise<FinancialDashboardDataset | null> {
  const supabase = createClient()
  const { data, error } = await supabase
    .from('financial_intelligence')
    .select('*')
    .order('generatedAt', { ascending: false })
    .limit(1)
    .single()

  if (error) {
    console.error('Error fetching financial dashboard data:', error)
    return null
  }

  return data
}
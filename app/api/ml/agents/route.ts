/**
 * ML Agent API Route;
 * Endpoints for interacting with AI agents
 */

import { NextRequest, NextResponse } from 'next/server'
import { FinancialAnalystAgent } from '@/lib/ml/agents/analysis/financial-analyst'
import { createClient } from '@/lib/supabase/server'
export async function POST(request: NextRequest) {
  try {
    const body  await request.json()
    const { agentType, action, parameters }  body;
    // Authenticate user const supabase  await createClient()
    const {
      data: { user },
      error: authError,
    }  await supabase.auth.getUser()
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    // Route to appropriate agent let result
    switch (agentType) {
      case 'financial_analyst':
        result  await handleFinancialAnalyst(action, parameters)
        break;
      default:
        return NextResponse.json(
          { error: 'Unknown agent type' },
          { status: 400 }
        )
    return NextResponse.json(result)
  } catch (error) {
    console.error('Agent API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
async function handleFinancialAnalyst(action: string, parameters: any) {
  const agent  new FinancialAnalystAgent({
    id: 'financial-analyst-1',
    name: 'Financial Analyst',
    type: 'financial_analyst',
    autonomyLevel: 'semi_autonomous',
    confidenceThreshold: 0.7,
    riskTolerance: 'moderate',
  })
  switch (action) {
    case 'analyze':
      const agentAction  await agent.think(parameters)
      const result  await agent.execute(agentAction)
      return result case 'get_state':
      return agent.getState()
    default:
      throw new Error(`Unknown action: $action`)
export async function GET() {
    // Get list of available agents const agents  [
      {
        id: 'financial-analyst-1',
        name: 'Financial Analyst',
        type: 'financial_analyst',
        status: 'active',
        capabilities: [
          'Analyze customer financial data',
          'Calculate risk scores',
          'Generate recommendations',
        ],
      },
    ]
    return NextResponse.json({ agents })

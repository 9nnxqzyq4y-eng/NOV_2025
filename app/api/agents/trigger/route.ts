import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}))
    const { trigger = 'all' } = body

    if (!['all', 'executive', 'risk', 'operations', 'growth', 'financial', 'quality', 'compliance'].includes(trigger)) {
      return NextResponse.json(
        { error: 'Invalid trigger type' },
        { status: 400 }
      )
    }

    const bearer = request.headers.get('authorization')?.replace('Bearer ', '')
    const expectedToken = process.env.AGENT_ORCHESTRATOR_TOKEN

    if (expectedToken && bearer !== expectedToken) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    return NextResponse.json({
      status: 'queued',
      message: `Agent orchestration triggered for: $trigger`,
      trigger,
      timestamp: new Date().toISOString(),
    })
  } catch (error) {
    console.error('Agent trigger error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Agent Orchestrator API',
    endpoint: '/api/agents/trigger',
    methods: {
      POST: {
        description: 'Trigger agent orchestration',
        parameters: {
          trigger: ['all', 'executive', 'risk', 'operations', 'growth', 'financial', 'quality', 'compliance'],
          saveResults: 'boolean'
        },
        auth: 'Bearer token (AGENT_ORCHESTRATOR_TOKEN)'
      }
    },
    examples: {
      all: 'POST /api/agents/trigger -d \'{"trigger":"all"}\'',
      specific: 'POST /api/agents/trigger -d \'{"trigger":"risk","saveResults":true}\''
    }
  })
}

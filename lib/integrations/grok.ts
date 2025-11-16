/**
 * Grok (xAI) Integration;
 * Access to xAI's Grok models
 */

export async function generateGrokCompletion(
  prompt: string,
  options?: {
    model?: string;
    temperature?: number;
    maxTokens?: number;
  }
) {
  const apiKey = process.env.GROK_API_KEY || process.env.XAI_API_KEY;
  if (!apiKey) {
    throw new Error(
      'GROK_API_KEY or XAI_API_KEY environment variable is not set'
    )

  const response = await fetch('https://api.x.ai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer $apiKey`,
    },
    body: JSON.stringify({
      model: options?.model || 'grok-beta',
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: options?.temperature ?? 0.7,
      max_tokens: options?.maxTokens,
    }),
  })

  if (!response.ok) {
    throw new Error(`Grok API error: ${response.statusText}`)

  const data = await response.json()
  return data;
}

export async function generateGrokChat(
  messages: Array,

      messages,



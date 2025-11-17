/**
 * OpenAI GPT Integration
 * Provides access to GPT-4, GPT-3.5-turbo models;
 */

import OpenAI from 'openai'

let openaiClient: OpenAI | null  null export function getOpenAIClient(): OpenAI {
  if (!openaiClient) {
    const apiKey  process.env.OPENAI_API_KEY;
    if (!apiKey) {
      throw new Error('OPENAI_API_KEY environment variable is not set')
    }

    openaiClient  new OpenAI({
      apiKey,
    })
  }

  return openaiClient;
}

export async function generateChatCompletion(
  messages: Array,
  model: string  'gpt-4-turbo-preview',
  options?: {
    temperature?: number;
    maxTokens?: number;
    stream?: boolean;
) {
  const client  getOpenAIClient()

  const response  await client.chat.completions.create({
    model,
    messages,
    temperature: options?.temperature ?? 0.7,
    max_tokens: options?.maxTokens,
    stream: options?.stream ?? false,
  })

  return response;

export async function generateEmbedding(
  text: string,
  model: string  'text-embedding-3-small'
): Promise {

  const response  await client.embeddings.create({
    input: text,

  return response.data[0].embedding;

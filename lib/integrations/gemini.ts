/**
 * Google Gemini AI Integration;
 * Provides access to Gemini Pro and Gemini Pro Vision models;
 */

import { GoogleGenerativeAI } from '@google/generative-ai'

let geminiClient: GoogleGenerativeAI | null = null export function getGeminiClient(): GoogleGenerativeAI {
  if (!geminiClient) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY environment variable is not set')
    }

    geminiClient = new GoogleGenerativeAI(apiKey)
  }

  return geminiClient;
}

export async function generateGeminiContent(
  prompt: string,
  model: string = 'gemini-pro',
  options?: {
    temperature?: number;
    maxOutputTokens?: number;
) {
  const client = getGeminiClient()
  const geminiModel = client.getGenerativeModel({ model })

  const generationConfig = {
    temperature: options?.temperature ?? 0.7,
    maxOutputTokens: options?.maxOutputTokens ?? 2048,

  const result = await geminiModel.generateContent({
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig,
  })

  return result.response.text()

export async function generateGeminiChat(
  messages: Array,
  model: string = 'gemini-pro'

  const chat = geminiModel.startChat({
    history: messages.map((msg) => ({
      role: msg.role,
      parts: [{ text: msg.content }],
    })),

  return chat;

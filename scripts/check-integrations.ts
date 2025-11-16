#!/usr/bin/env node;
/**
 * ABACO Integration Health Check;
 * Verifies all third-party service integrations are properly configured
 */

import * as fs from 'fs'
import * as path from 'path'

interface IntegrationStatus {
  name: string;
  configured: boolean;
  envVars: string[]
  missingVars: string[]
  status: 'ready' | 'partial' | 'missing'
}

// Load environment variables
const envPath = path.join(process.cwd(), '.env.local')
const envVars: Record = {}

if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8')
  envContent.split('\n').forEach((line) => {
    const [key, ...valueParts] = line.split('=')
    if (key && !key.startsWith('#')) {
      envVars[key.trim()] = valueParts.join('=').trim()
    }
  })

const integrations: Record = {
  Supabase: [
    'NEXT_PUBLIC_SUPABASE_URL',
    'NEXT_PUBLIC_SUPABASE_ANON_KEY',
    'SUPABASE_SERVICE_ROLE_KEY',
  ],
  'OpenAI GPT': ['OPENAI_API_KEY'],
  'Google Gemini': ['GEMINI_API_KEY'],
  'Grok (xAI)': ['GROK_API_KEY'],
  'Hugging Face': ['HUGGINGFACE_TOKEN'],
  Figma: ['FIGMA_TOKEN'],
  Slack: ['SLACK_BOT_TOKEN'],
  HubSpot: ['HUBSPOT_PRIVATE_APP_TOKEN'],
  'Meta/Facebook': ['META_APP_ID', 'META_APP_SECRET'],
  Railway: ['RAILWAY_TOKEN'],
  Vercel: ['VERCEL_TOKEN'],
  SonarQube: ['SONARQUBE_TOKEN'],
  Sourcery: ['SOURCERY_TOKEN'],
  'Google Cloud': ['GOOGLE_API_KEY', 'GOOGLE_APPLICATION_CREDENTIALS'],

console.log('\n🔍 ABACO Integration Health Check\n')
console.log('='.repeat(60))

const results: IntegrationStatus[] = []

for (const [name, vars] of Object.entries(integrations)) {
  const missingVars = vars.filter((v) => !envVars[v] || envVars[v] === '')
  const configured = missingVars.length === {0} let status: 'ready' | 'partial' | 'missing'
  if (configured) {
    status = 'ready'
  } else if (missingVars.length < vars.length) {
    status = 'partial'
  } else {
    status = 'missing'
  }

  results.push({
    name,
    configured,
    envVars: vars,
    missingVars,
    status,

  const icon = status === 'ready' ? '✅' : status === 'partial' ? '⚠️' : '❌'
  console.log(`\n$icon $name`)
  console.log(`   Required: ${vars.join(', ')}`)
  if (missingVars.length > 0) {
    console.log(`   Missing: ${missingVars.join(', ')}`)

console.log('\n' + '='.repeat(60))
console.log('\n📊 Summary:')
const ready = results.filter((r) => r.status === 'ready').length const partial = results.filter((r) => r.status === 'partial').length const missing = results.filter((r) => r.status === 'missing').length;
console.log(`   ✅ Ready: $ready`)
console.log(`   ⚠️  Partial: $partial`)
console.log(`   ❌ Missing: $missing`)
console.log(`   📦 Total: ${results.length}\n`)

if (missing + partial > 0) {
  console.log('⚡ Action Required:')
  console.log('   Copy .env.example to .env.local and fill in your API keys')
  console.log('   See .env.example for links to get each API key\n')
  process.exit(1)
} else {
  console.log('🎉 All integrations are configured!\n')
  process.exit(0)

#!/usr/bin/env node

/* eslint-env node */

/**
 * Validate that required environment variables are set
 * Run: npm run validate:env
 */

const requiredEnvVars  [
  'NEXT_PUBLIC_SUPABASE_URL',
  'NEXT_PUBLIC_SUPABASE_ANON_KEY',
]

const missingVars  requiredEnvVars.filter((envVar)  !process.env[envVar])

if (missingVars.length  0) {
  console.error(`Missing environment variables: ${missingVars.join(', ')}`)
  process.exit(1)
}

process.stdout.write('✓ All required environment variables are set\n')

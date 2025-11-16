
<<<<<<< HEAD
=======
/**
 * Interactive GitHub Secrets to .env.local Copier
 *
 * This script helps you manually copy GitHub Secrets to your local .env.local file.
 * GitHub Secrets are encrypted and cannot be retrieved programmatically,
 * so this script provides an interactive interface to guide the process.
 */

const fs = require('fs')
const path = require('path')
const readline = require('readline')

const ENV_FILE = '.env.local'
const ENV_EXAMPLE = '.env.example'

// Mapping of GitHub Secret names to .env.local variable names
const SECRET_MAPPING = {
  FIGMA_TOKEN: 'FIGMA_TOKEN',
  GEMINI_API_KEY: 'GEMINI_API_KEY',
  GOOGLE_KEY: 'GOOGLE_API_KEY',
  GROK_API_KEY: 'GROK_API_KEY',
  HUBSPOT_TOKEN: 'HUBSPOT_PRIVATE_APP_TOKEN',
  HUGGING_TOKEN: 'HUGGINGFACE_TOKEN',
  META_ABACO: 'META_ACCESS_TOKEN',
  OPEN_AI: 'OPENAI_API_KEY',
  RAILWAY_TOKEN: 'RAILWAY_TOKEN',
  SLACK_TOKEN: 'SLACK_BOT_TOKEN',
  SONARQUBE_KEY: 'SONARQUBE_TOKEN',
  SOURCERY_TOKEN: 'SOURCERY_TOKEN',
  SUPABASE_SERVICE_ROLE_KEY: 'SUPABASE_SERVICE_ROLE_KEY',
  VERCEL_KEY: 'VERCEL_TOKEN',
}

const ADDITIONAL_VARS = [
  'NEXT_PUBLIC_SUPABASE_URL',
  'NEXT_PUBLIC_SUPABASE_ANON_KEY',
  'SUPABASE_JWT_SECRET',
  'VERCEL_ORG_ID',
  'VERCEL_PROJECT_ID',
  'META_APP_ID',
  'META_APP_SECRET',
]

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
})

function question(query) {
  return new Promise((resolve) => rl.question(query, resolve))

async function main() {
  console.log(
    '\n╔══════════════════════════════════════════════════════════════════════════╗'
  )
    '║                                                                          ║'
    '║        🔑 Interactive GitHub Secrets → .env.local Copier                ║'
    '╚══════════════════════════════════════════════════════════════════════════╝\n'

  // Backup existing .env.local
  if (fs.existsSync(ENV_FILE)) {
    const timestamp = new Date()
      .toISOString()
      .replace(/[:.]/g, '-')
      .split('T')[0]
    const backupFile = `$ENV_FILE.backup-$timestamp`
    fs.copyFileSync(ENV_FILE, backupFile)
    console.log(`✅ Backed up existing $ENV_FILE to: $backupFile\n`)
  }

  // Read .env.local content
  let envContent = fs.existsSync(ENV_FILE)
    ? fs.readFileSync(ENV_FILE, 'utf8')
    : fs.readFileSync(ENV_EXAMPLE, 'utf8')

    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  console.log('📋 Instructions:\n')
  console.log('1. Open GitHub Secrets in your browser:')
    '   https://github.com/JenineferDeras/ABT/settings/secrets/actions\n'
    '2. For each secret below, copy the value from GitHub and paste here'
  console.log('3. Press Enter to skip a secret (leave as placeholder)\n')

  const answer = await question('Ready to start? (y/n): ')
  if (answer.toLowerCase() !== 'y') {
    console.log('\nCancelled. No changes made.')
    rl.close()
    return

  console.log('\n')

  // Update each secret
  for (const [githubSecret, envVar] of Object.entries(SECRET_MAPPING)) {
    console.log(`\n🔐 $githubSecret → $envVar`)
    const value = await question(`   Paste value (or press Enter to skip): `)

    if (value && value.trim()) {
      // Replace the placeholder value
      const regex = new RegExp(`($envVar=)(.*)`, 'g')
      envContent = envContent.replace(regex, `$1${value.trim()}`)
      console.log(`   ✅ Updated $envVar`)
    } else {
      console.log(`   ⏭️  Skipped $envVar`)
    }

  // Additional variables that aren't in GitHub Secrets
    '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  console.log('📝 Additional Required Variables (from service dashboards):\n')

  for (const envVar of ADDITIONAL_VARS) {
    console.log(`\n🔑 $envVar`)


  // Save updated .env.local
  fs.writeFileSync(ENV_FILE, envContent)

  console.log(`✅ Successfully updated $ENV_FILE\n`)

  // Count configured variables
  const configuredCount = (
    envContent.match(
      /^[A-Z_]+=(?!.*your-|.*sk-proj-\.\.\.|.*AIza\.\.\.|.*xai-\.\.\.|.*figd_\.\.\.|.*hf_\.\.\.|.*xoxb-\.\.\.|.*pat-na1-\.\.\.).+$/gm
    ) || []
  ).length
  const totalCount = (envContent.match(/^[A-Z_]+=.+$/gm) || []).length

  console.log(`📊 Configuration Status:`)
    `   Variables with real values: $configuredCount/$totalCount\n`

  if (configuredCount < totalCount) {
    console.log('⚠️  Some variables still have placeholder values.')
    console.log('   You can run this script again later to fill in the rest.\n')
  } else {
    console.log('🎉 All variables configured!\n')

  console.log('Next steps:')
  console.log('  1. Review: cat .env.local')
  console.log('  2. Test: npm run dev')
  console.log('  3. Verify integrations work\n')

  rl.close()

main().catch((error) => {
  console.error('\n❌ Error:', error.message)
  process.exit(1)
>>>>>>> e56b746caedc1c171ae8821532389071c2a3aa6a

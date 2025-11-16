#!/bin/bash

# ==============================================================================
# Automated GitHub Secrets → .env.local Sync
# ==============================================================================
# Uses GitHub CLI to fetch secrets and populate .env.local
# Note: This uses a workaround since secrets can't be retrieved directly

set -e

REPO="JenineferDeras/ABT"
ENV_FILE=".env.local"

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║        🚀 Automated GitHub Secrets → .env.local Sync                    ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not installed. Install with: brew install gh"
    exit 1
fi

# Backup
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "${ENV_FILE}.backup-$(date +%Y%m%d-%H%M%S)"
    echo "✅ Backed up $ENV_FILE"
fi

# Copy template
cp .env.example "$ENV_FILE"
echo "✅ Created $ENV_FILE from template"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Fetching secrets from GitHub Actions runs..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  GitHub Secrets are encrypted and cannot be retrieved via API."
echo ""
echo "SOLUTION: Use environment variables from latest successful workflow run"
echo "          (Secrets are exposed as env vars during CI/CD execution)"
echo ""

# Function to update .env.local
update_env() {
    local KEY=$1
    local VALUE=$2
    
    if [ -n "$VALUE" ] && [ "$VALUE" != "***" ]; then
        # Use sed to replace the placeholder
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|^${KEY}=.*|${KEY}=${VALUE}|g" "$ENV_FILE"
        else
            # Linux
            sed -i "s|^${KEY}=.*|${KEY}=${VALUE}|g" "$ENV_FILE"
        fi
        echo "✅ Updated: $KEY"
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 MANUAL STEP REQUIRED:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Since GitHub Secrets cannot be retrieved programmatically,"
echo "please run ONE of these commands:"
echo ""
echo "Option 1: Interactive Script (RECOMMENDED)"
echo "──────────────────────────────────────────"
echo "  node scripts/sync-secrets-interactive.js"
echo ""
echo "Option 2: Manual Copy"
echo "──────────────────────────────────────────"
echo "  1. Open: https://github.com/$REPO/settings/secrets/actions"
echo "  2. Edit: $ENV_FILE"
echo "  3. Copy each secret value from GitHub to the file"
echo ""
echo "Option 3: Use This Helper Script"
echo "──────────────────────────────────────────"
echo "  I'll guide you through each secret one by one..."
echo ""

read -p "Would you like to enter secrets now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📝 Enter Secret Values (paste from GitHub Secrets page)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Open in browser: https://github.com/$REPO/settings/secrets/actions"
    echo ""
    
    # Figma
    read -p "FIGMA_TOKEN: " FIGMA_TOKEN
    [ -n "$FIGMA_TOKEN" ] && update_env "FIGMA_TOKEN" "$FIGMA_TOKEN"
    
    # Gemini
    read -p "GEMINI_API_KEY: " GEMINI_API_KEY
    [ -n "$GEMINI_API_KEY" ] && update_env "GEMINI_API_KEY" "$GEMINI_API_KEY"
    
    # Google
    read -p "GOOGLE_API_KEY (GOOGLE_KEY in GitHub): " GOOGLE_API_KEY
    [ -n "$GOOGLE_API_KEY" ] && update_env "GOOGLE_API_KEY" "$GOOGLE_API_KEY"
    
    # Grok
    read -p "GROK_API_KEY: " GROK_API_KEY
    [ -n "$GROK_API_KEY" ] && update_env "GROK_API_KEY" "$GROK_API_KEY" && \
        update_env "XAI_API_KEY" "$GROK_API_KEY" && \
        update_env "NEXT_PUBLIC_GROK_API_KEY" "$GROK_API_KEY"
    
    # HubSpot
    read -p "HUBSPOT_PRIVATE_APP_TOKEN (HUBSPOT_TOKEN in GitHub): " HUBSPOT_TOKEN
    [ -n "$HUBSPOT_TOKEN" ] && update_env "HUBSPOT_PRIVATE_APP_TOKEN" "$HUBSPOT_TOKEN"
    
    # Hugging Face
    read -p "HUGGINGFACE_TOKEN (HUGGING_TOKEN in GitHub): " HUGGING_TOKEN
    [ -n "$HUGGING_TOKEN" ] && update_env "HUGGINGFACE_TOKEN" "$HUGGING_TOKEN"
    
    # Meta
    read -p "META_ACCESS_TOKEN (META_ABACO in GitHub): " META_ABACO
    [ -n "$META_ABACO" ] && update_env "META_ACCESS_TOKEN" "$META_ABACO"
    
    # OpenAI
    read -p "OPENAI_API_KEY (OPEN_AI in GitHub): " OPEN_AI
    [ -n "$OPEN_AI" ] && update_env "OPENAI_API_KEY" "$OPEN_AI"
    
    # Railway
    read -p "RAILWAY_TOKEN: " RAILWAY_TOKEN
    [ -n "$RAILWAY_TOKEN" ] && update_env "RAILWAY_TOKEN" "$RAILWAY_TOKEN"
    
    # Slack
    read -p "SLACK_BOT_TOKEN (SLACK_TOKEN in GitHub): " SLACK_TOKEN
    [ -n "$SLACK_TOKEN" ] && update_env "SLACK_BOT_TOKEN" "$SLACK_TOKEN"
    
    # SonarQube
    read -p "SONARQUBE_TOKEN (SONARQUBE_KEY in GitHub): " SONARQUBE_KEY
    [ -n "$SONARQUBE_KEY" ] && update_env "SONARQUBE_TOKEN" "$SONARQUBE_KEY"
    
    # Sourcery
    read -p "SOURCERY_TOKEN: " SOURCERY_TOKEN
    [ -n "$SOURCERY_TOKEN" ] && update_env "SOURCERY_TOKEN" "$SOURCERY_TOKEN"
    
    # Supabase
    read -p "SUPABASE_SERVICE_ROLE_KEY: " SUPABASE_SERVICE_ROLE_KEY
    [ -n "$SUPABASE_SERVICE_ROLE_KEY" ] && update_env "SUPABASE_SERVICE_ROLE_KEY" "$SUPABASE_SERVICE_ROLE_KEY" && \
        update_env "SUPABASE_SERVICE_KEY" "$SUPABASE_SERVICE_ROLE_KEY"
    
    # Vercel
    read -p "VERCEL_TOKEN (VERCEL_KEY in GitHub): " VERCEL_KEY
    [ -n "$VERCEL_KEY" ] && update_env "VERCEL_TOKEN" "$VERCEL_KEY"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📝 Additional Variables (from service dashboards)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Supabase additional
    read -p "NEXT_PUBLIC_SUPABASE_URL: " SUPABASE_URL
    [ -n "$SUPABASE_URL" ] && update_env "NEXT_PUBLIC_SUPABASE_URL" "$SUPABASE_URL" && \
        update_env "SUPABASE_URL" "$SUPABASE_URL" && \
        update_env "SUPABASE_SERVICE_ROLE_URL" "$SUPABASE_URL"
    
    read -p "NEXT_PUBLIC_SUPABASE_ANON_KEY: " SUPABASE_ANON_KEY
    [ -n "$SUPABASE_ANON_KEY" ] && update_env "NEXT_PUBLIC_SUPABASE_ANON_KEY" "$SUPABASE_ANON_KEY"
    
    read -p "SUPABASE_JWT_SECRET: " SUPABASE_JWT_SECRET
    [ -n "$SUPABASE_JWT_SECRET" ] && update_env "SUPABASE_JWT_SECRET" "$SUPABASE_JWT_SECRET"
    
    # Vercel additional
    read -p "VERCEL_ORG_ID: " VERCEL_ORG_ID
    [ -n "$VERCEL_ORG_ID" ] && update_env "VERCEL_ORG_ID" "$VERCEL_ORG_ID"
    
    read -p "VERCEL_PROJECT_ID: " VERCEL_PROJECT_ID
    [ -n "$VERCEL_PROJECT_ID" ] && update_env "VERCEL_PROJECT_ID" "$VERCEL_PROJECT_ID"
    
    echo ""
    echo "✅ Secrets updated in $ENV_FILE"
    echo ""
fi

# Count configured vars
CONFIGURED=$(grep -E "^[A-Z_]+=(?!.*your-|.*sk-proj-\.\.\.|.*AIza\.\.\.|.*xai-\.\.\.).+" "$ENV_FILE" 2>/dev/null | wc -l | tr -d ' ')
TOTAL=$(grep -E "^[A-Z_]+=.+" "$ENV_FILE" 2>/dev/null | wc -l | tr -d ' ')

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Configuration Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Variables configured: $CONFIGURED/$TOTAL"
echo ""
echo "Next steps:"
echo "  1. Review: cat .env.local | head -50"
echo "  2. Test: npm run dev"
echo "  3. Verify integrations work"
echo ""

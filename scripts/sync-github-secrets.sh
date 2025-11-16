#!/bin/bash

# ==============================================================================
# Sync GitHub Secrets to Local .env.local
# ==============================================================================
# This script retrieves GitHub repository secrets and populates .env.local
# Requires: GitHub CLI (gh) installed and authenticated

set -e

REPO_OWNER="JenineferDeras"
REPO_NAME="ABT"
ENV_FILE=".env.local"

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                          ║"
echo "║           🔑 Syncing GitHub Secrets to .env.local                        ║"
echo "║                                                                          ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ ERROR: GitHub CLI (gh) is not installed"
    echo ""
    echo "Install with:"
    echo "  brew install gh"
    echo ""
    echo "Or visit: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ ERROR: Not authenticated with GitHub CLI"
    echo ""
    echo "Authenticate with:"
    echo "  gh auth login"
    exit 1
fi

echo "✅ GitHub CLI authenticated"
echo ""

# Backup existing .env.local
if [ -f "$ENV_FILE" ]; then
    BACKUP_FILE="${ENV_FILE}.backup-$(date +%Y%m%d-%H%M%S)"
    cp "$ENV_FILE" "$BACKUP_FILE"
    echo "✅ Backed up existing .env.local to: $BACKUP_FILE"
else
    echo "⚠️  No existing .env.local found, creating new one"
fi

# Start with the template
cp .env.example "$ENV_FILE"
echo "✅ Created .env.local from .env.example"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Retrieving GitHub Secrets..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to update env variable
update_env() {
    local SECRET_NAME=$1
    local ENV_VAR_NAME=$2
    
    echo -n "Fetching $SECRET_NAME... "
    
    # Get secret value (note: this may not work as secrets are encrypted)
    # GitHub doesn't allow retrieving secret values via CLI for security
    # We'll need to use a different approach
    
    echo "⚠️  Cannot retrieve (GitHub Secrets are encrypted)"
}

# Map GitHub Secrets to .env.local variables
echo "⚠️  IMPORTANT: GitHub Secrets cannot be retrieved programmatically"
echo "              (they are encrypted and hidden for security)"
echo ""
echo "You have two options:"
echo ""
echo "1. Manual Copy (RECOMMENDED):"
echo "   - Go to: https://github.com/$REPO_OWNER/$REPO_NAME/settings/secrets/actions"
echo "   - Click each secret and copy the value"
echo "   - Paste into .env.local file"
echo ""
echo "2. Use GitHub Actions (for CI/CD only):"
echo "   - Secrets automatically populate in GitHub Actions workflows"
echo "   - NOT available for local development"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Secrets to Copy from GitHub to .env.local:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "GitHub Secret Name          → .env.local Variable"
echo "─────────────────────────────────────────────────────────────────────"
echo "FIGMA_TOKEN                 → FIGMA_TOKEN"
echo "GEMINI_API_KEY              → GEMINI_API_KEY"
echo "GOOGLE_KEY                  → GOOGLE_API_KEY"
echo "GROK_API_KEY                → GROK_API_KEY"
echo "HUBSPOT_TOKEN               → HUBSPOT_PRIVATE_APP_TOKEN"
echo "HUGGING_TOKEN               → HUGGINGFACE_TOKEN"
echo "META_ABACO                  → META_ACCESS_TOKEN (or META_APP_ID, etc.)"
echo "OPEN_AI                     → OPENAI_API_KEY"
echo "RAILWAY_TOKEN               → RAILWAY_TOKEN"
echo "SLACK_TOKEN                 → SLACK_BOT_TOKEN"
echo "SONARQUBE_KEY               → SONARQUBE_TOKEN"
echo "SOURCERY_TOKEN              → SOURCERY_TOKEN"
echo "SUPABASE_SERVICE_ROLE_KEY   → SUPABASE_SERVICE_ROLE_KEY"
echo "VERCEL_KEY                  → VERCEL_TOKEN"
echo ""
echo "Note: You'll also need:"
echo "  - NEXT_PUBLIC_SUPABASE_URL (from Supabase dashboard)"
echo "  - NEXT_PUBLIC_SUPABASE_ANON_KEY (from Supabase dashboard)"
echo "  - SUPABASE_JWT_SECRET (from Supabase dashboard)"
echo "  - VERCEL_ORG_ID and VERCEL_PROJECT_ID (from Vercel dashboard)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Open in browser: https://github.com/$REPO_OWNER/$REPO_NAME/settings/secrets/actions"
echo "2. Open in editor: $ENV_FILE"
echo "3. Copy each secret value from GitHub and paste into .env.local"
echo "4. Run: npm run dev (to test)"
echo ""
echo "✅ Template ready: $ENV_FILE"
echo ""

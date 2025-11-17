#!/bin/bash

set -e
echo "🚂 Railway Deployment Script"
echo ""
# Check if Railway CLI is installed
if ! command -v railway & /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi
# Run tests
echo "🧪 Running tests..."
npm test -- --passWithNoTests || {
    echo "❌ Tests failed. Please fix errors before deploying."
    exit 1
}
# Deploy
echo "🚀 Deploying to Railway..."
railway up
# Get deployment URL
echo "🌐 Deployment URL:"
railway domain
echo "✅ Deployment complete!"
echo "📊 View logs with: railway logs"

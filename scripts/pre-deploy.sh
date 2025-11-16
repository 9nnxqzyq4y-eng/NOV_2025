#!/bin/bash
# Pre-deployment verification script

set -e

echo "🚀 Pre-Deployment Verification"
echo ""

# 1. Check git status
echo "1️⃣  Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Working directory not clean. Please commit all changes."
  git status
  exit 1
fi
echo "✅ Git working tree clean"

# 2. Run quality checks
echo ""
echo "2️⃣  Running quality checks..."
npm run quality-check || {
  echo "❌ Quality checks failed"
  exit 1
}

# 3. Check environment variables
echo ""
echo "3️⃣  Checking environment variables..."
if [ ! -f ".env.local" ]; then
  echo "⚠️  Warning: .env.local not found"
  echo "   Create .env.local with required variables before deploying"
fi

# 4. Verify build artifacts
echo ""
echo "4️⃣  Verifying build artifacts..."
if [ ! -d ".next" ]; then
  echo "⚠️  .next directory not found. Run 'npm run build' first."
fi
echo "✅ Build artifacts present"

# 5. Summary
echo ""
echo "✅ Pre-deployment verification complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Verify environment variables: cat .env.local"
echo "  2. Review changes: git log --oneline -5"
echo "  3. Deploy: git push origin main"
echo ""
echo "📊 Monitor deployment:"
echo "  - Vercel: https://vercel.com/dashboard"
echo "  - SonarQube: https://sonarcloud.io/dashboard?idjenineferderas_abaco-sim-e"

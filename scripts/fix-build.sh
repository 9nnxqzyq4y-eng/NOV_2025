#!/bin/bash
# Complete build fix script

set -e

echo "🔧 Fixing build issues..."
echo ""

# Step 1: Install missing dependencies
echo "1️⃣  Installing missing dependencies..."
npm install tailwindcss-animate

# Step 2: Clear caches
echo ""
echo "2️⃣  Clearing caches..."
rm -rf .next node_modules/.cache

# Step 3: Run type check
echo ""
echo "3️⃣  Running type check..."
npm run type-check 2&1 || {
  echo "⚠️  Type check failed - check lib/abaco-strategy-2026.ts"
  exit 1
}

# Step 4: Run linting
echo ""
echo "4️⃣  Running ESLint..."
npm run lint -- --fix

# Step 5: Build
echo ""
echo "5️⃣  Building project..."
npm run build || {
  echo "❌ Build failed"
  exit 1
}

echo ""
echo "✅ Build fixes complete!"
echo ""
echo "Next steps:"
echo "1. Verify .env.local has correct Supabase URL and keys"
echo "2. Start dev server: npm run dev"
echo "3. Or use specific port: PORT3001 npm run dev"

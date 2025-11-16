#!/bin/bash
# Script to identify and help fix SonarQube issues

set -e

echo "🔍 Analyzing SonarQube issues..."
echo ""
echo "Common issues to fix:"
echo ""

# Check for unused variables (eslint should catch these)
echo "1. Running ESLint to catch unused variables and common issues..."
npm run lint 2&1 | head -20 || echo "   (Some linting issues found)"

echo ""
echo "2. Checking for any 'any' types in TypeScript..."
grep -r ":\s*any" app components lib --include"*.ts" --include"*.tsx" | head -10 || echo "   ✅ No 'any' types found"

echo ""
echo "3. Checking for empty catch blocks..."
grep -r "catch\s*{" app components lib --include"*.ts" --include"*.tsx" -A 1 | grep "^--$" || echo "   ✅ No empty catch blocks"

echo ""
echo "4. Running type check..."
npm run type-check 2&1 | tail -5 || echo "   ✅ Type checking passed"

echo ""
echo "📊 To see full SonarQube report:"
echo "   👉 https://sonarcloud.io/project/issues?idjenineferderas_abaco-sim-e"

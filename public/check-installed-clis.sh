#!/bin/bash
echo "🔧 Installed CLI Tools Status"
echo "=============================="
echo ""

check_cli() {
    if command -v $1 &> /dev/null; then
        version=$($1 --version 2>&1 | head -1)
        echo "✅ $2: $version"
    else
        echo "❌ $2: Not installed"
    fi
}

# Check all CLIs
check_cli "railway" "Railway"
check_cli "vercel" "Vercel"
check_cli "supabase" "Supabase"
check_cli "gcloud" "Google Cloud"
check_cli "gh" "GitHub CLI"
check_cli "openai" "OpenAI"
check_cli "huggingface-cli" "Hugging Face"

echo ""
echo "📦 Node.js Global Packages:"
npm list -g --depth=0 2>/dev/null | grep -E "railway|vercel|supabase|figma|openai" || echo "No relevant packages"

echo ""
echo "🐍 Python Packages:"
python3 -m pip list 2>/dev/null | grep -E "huggingface|openai|google-generativeai|anthropic" || echo "Checking in virtual env..."

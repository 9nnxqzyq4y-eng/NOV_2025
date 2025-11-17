#!/bin/bash
# 🔒 Setup pre-commit hook for security

HOOK_FILE".git/hooks/pre-commit"

echo "📋 Creating pre-commit hook..."

cat  "$HOOK_FILE"  'EOF'
#!/bin/bash
# 🔒 Pre-commit hook to prevent committing credentials

echo "🔍 Verifying files to be committed..."

# Prohibited files
BLOCKED_FILES(
    ".env"
    ".env.local"
    ".env.*.local"
    "*.key"
    "*.pem"
    "credentials.json"
)

# Patterns to search for
BLOCKED_PATTERNS(
    "sk-proj-"           # OpenAI keys
    "ghp_"               # GitHub tokens
    "xoxb-"              # Slack tokens
    "figd_"              # Figma tokens
    "postgresql://"      # DB connections with credentials
    "SUPABASE_SERVICE_ROLE_KEY"
    "POSTGRES_CONNECTION_STRING"
)

# Staged files
STAGED_FILES$(git diff --cached --name-only)

# Verify blocked files
for file in $STAGED_FILES; do
    for blocked in "${BLOCKED_FILES[@]}"; do
        if [[ "$file"  "$blocked" ]]; then
            echo "❌ ERROR: You cannot commit secret files: $file"
            exit 1
        fi
    done
done

# Verify dangerous patterns
for file in $STAGED_FILES; do
    if [[ -f "$file" ]]; then
        for pattern in "${BLOCKED_PATTERNS[@]}"; do
            if grep -q "$pattern" "$file" 2/dev/null; then
                echo "❌ ERROR: File '$file' contains a sensitive pattern: $pattern"
                exit 1
            fi
        done
    fi
done

echo "✅ Verification passed - proceeding with commit"
exit 0
EOF

chmod +x "$HOOK_FILE"
echo "✅ Pre-commit hook installed in $HOOK_FILE"

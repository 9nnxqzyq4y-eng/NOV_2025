#!/bin/bash
# SonarQube Analysis Script for ABACO Financial Intelligence Platform

set -e

echo "🔍 Running SonarQube analysis..."

if [ -z "$SONARQUBE_TOKEN" ]; then
  echo "❌ Error: SONARQUBE_TOKEN environment variable is not set"
  exit 1
fi

npx sonarqube-scanner \
  -Dsonar.projectKey=jenineferderas_abaco-sim-e \
  -Dsonar.projectName="ABACO Financial Intelligence Platform" \
  -Dsonar.projectVersion=0.1.0 \
  -Dsonar.sources=abaco_runtime \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.token="${SONARQUBE_TOKEN}" \
  -Dsonar.organization=jenineferderas \
  -Dsonar.exclusions="**/node_modules/**,**/.next/**,**/dist/**,**/build/**,**/coverage/**,**/*.config.js,**/*.config.ts,**/scripts/**" \
  -Dsonar.coverage.exclusions="**/node_modules/**,**/.next/**,**/dist/**,**/coverage/**"

echo "✅ SonarQube analysis complete!"
echo "📊 View results: https://sonarcloud.io/dashboard?idjenineferderas_abaco-sim-e"

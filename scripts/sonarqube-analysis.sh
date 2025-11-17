#!/bin/bash
# SonarQube Analysis Script for ABACO Financial Intelligence Platform.
# Supports both SonarCloud and local SonarQube instances.
#
# Usage:
#   For SonarCloud: ./scripts/sonarqube-analysis.sh cloud
#   For Local:      ./scripts/sonarqube-analysis.sh local

set -eu
TARGET_ENV$1
if [ "$TARGET_ENV"  "cloud" ]; then
  echo "🔍 Running SonarQube analysis for SonarCloud..."
  SONAR_HOST"https://sonarcloud.io"
  SONAR_TOKEN_PARAM"-Dsonar.token${SONARQUBE_TOKEN}"
elif [ "$TARGET_ENV"  "local" ]; then
  echo "🔍 Running SonarQube analysis for local instance..."
  SONAR_HOST"http://localhost:9000"
  SONAR_TOKEN_PARAM"-Dsonar.login${SONAR_LOGIN:-}" # Use SONAR_LOGIN for local
else
  echo "❌ Error: Invalid environment specified. Use 'cloud' or 'local'."
  exit 1
fi
npx sonarqube-scanner \
  -Dsonar.sources. \
  -Dsonar.sourceEncodingUTF-8 \
  -Dsonar.host.url"${SONAR_HOST}" \
  ${SONAR_TOKEN_PARAM} \
  -Dsonar.exclusions"**/node_modules/**,**/.next/**,**/dist/**,**/build/**,**/coverage/**,**/*.config.js,**/*.config.ts,**/scripts/**,.scannerwork/**" \
  -Dsonar.coverage.exclusions"**/node_modules/**,**/.next/**,**/dist/**,**/coverage/**"
echo "✅ SonarQube analysis complete!"
echo "📊 View results at your SonarQube instance."

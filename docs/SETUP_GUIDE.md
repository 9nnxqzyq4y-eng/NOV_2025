# Development Setup Guide

## Prerequisites

- Node.js 20.x
- npm (officially supported package manager)
- Supabase account
- Google Drive folder with financial data (optional)

## Environment Setup

### 1. Supabase Configuration

Create `.env.local`:

```bash
# Required - Get from https://supabase.com/dashboard/project/[project-ref]/settings/api
NEXT_PUBLIC_SUPABASE_URLhttps://[project-ref].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY[anon-key]
SUPABASE_SERVICE_ROLE_KEY[service-role-key]

# Optional - For Google Drive ingestion
GDRIVE_FOLDER_ID[folder-id]
GDRIVE_SERVICE_ACCOUNT{"type":"service_account",...}

# Optional - For Grok AI features
GROK_API_KEY[api-key]

### 2. Validate Environment

# Check that critical env vars are set
npm run validate:env

### 3. Database Setup

# Apply migrations
npx supabase db push

# Or run migrations manually in Supabase SQL editor

### 4. Start Development

npm run dev

## Testing

# Run all tests
npm run test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

## Deployment Validation

Before deploying, ensure:

1. All environment variables are set in deployment platform
1. `npm run type-check` passes
1. `npm run lint` passes (no errors)
1. `npm run build` succeeds
1. Tests pass: `npm run test -- run`


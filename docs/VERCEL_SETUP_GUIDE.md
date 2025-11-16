# Vercel Deployment Setup Guide

## Step 1: Create Vercel Token

1. **Open Vercel Tokens Page** (already opened in your browser):
   - URL: https://vercel.com/account/tokens
   - Or navigate: Vercel Dashboard → Settings → Tokens

1. **Create New Token**:
   - Click "Create Token" button
   - **Token Name**: `GitHub Actions - ABT`
   - **Scope**: Full Account (or select specific team if needed)
   - **Expiration**: No Expiration (recommended for CI/CD)
   - Click "Create Token"

1. **Copy Token Immediately**:
   - ⚠️ **IMPORTANT**: Copy the token NOW - you won't see it again!
   - Save it temporarily in a secure location (e.g., password manager)

## Step 2: Get Vercel Project IDs

### Option A: Using Vercel CLI (Recommended)

```bash
# Login to Vercel
vercel login

# Link project (run from project directory)
cd ~/Documents/GitHub/ABT
vercel link

# Get project settings
vercel project ls

The CLI will create a `.vercel/project.json` file with your `orgId` and `projectId`.

### Option B: From Vercel Dashboard

1. Go to your project: https://vercel.com/dashboard
1. Select "ABT" project
1. Go to **Settings** tab
1. **Project ID**: Found in Settings → General → Project ID
1. **Organization/Team ID**: Found in your account settings

### Option C: Manual Inspection

After running `vercel link`, check the generated file:

cat .vercel/project.json

You'll see:

```json
{
  "orgId": "team_xxxxxxxxxxxxx",
  "projectId": "prj_xxxxxxxxxxxxx"
}

## Step 3: Configure GitHub Secrets

1. **Open GitHub Secrets Page**:
   - URL: https://github.com/JenineferDeras/ABT/settings/secrets/actions
   - Or navigate: Repository → Settings → Secrets and variables → Actions

1. **Add Three Secrets**:

   ### Secret 1: VERCEL_TOKEN
   - Click "New repository secret"
   - Name: `VERCEL_TOKEN`
   - Value: [Paste the token from Step 1]
   - Click "Add secret"

   ### Secret 2: VERCEL_ORG_ID
   - Name: `VERCEL_ORG_ID`
   - Value: [Paste orgId from .vercel/project.json]

   ### Secret 3: VERCEL_PROJECT_ID
   - Name: `VERCEL_PROJECT_ID`
   - Value: [Paste projectId from .vercel/project.json]

## Step 4: Configure Vercel Environment Variables

You also need to add Supabase credentials to Vercel:

1. Go to: https://vercel.com/[your-project]/settings/environment-variables
1. Add the following variables:

   ### Production Supabase (Required)
   - `NEXT_PUBLIC_SUPABASE_URL`: Your production Supabase URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your production Supabase anon key
   - `SUPABASE_SERVICE_ROLE_KEY`: Your production Supabase service role key

   ### Optional (if using Grok AI)
   - `GROK_API_KEY`: Your Grok API key

### Where to Find Supabase Production Credentials

1. **Supabase Dashboard**: https://supabase.com/dashboard
1. Select your project
1. Go to **Settings** → **API**
1. Copy:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **Project API keys** → **anon public** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **Project API keys** → **service_role** → `SUPABASE_SERVICE_ROLE_KEY`

## Step 5: Re-enable Vercel Deployment Workflow

Once all secrets are configured, re-enable the workflow:

mv .github/workflows-disabled/deploy.yml .github/workflows/deploy.yml
git add .github/workflows/
git commit -m "ci: re-enable Vercel deployment workflow"
git push origin main

## Step 6: Test Deployment

1. **Check GitHub Actions**:
   - URL: https://github.com/JenineferDeras/ABT/actions
   - The "Deploy to Vercel" workflow should now run successfully

1. **Manual Deployment** (optional):
   ```bash
   cd ~/Documents/GitHub/ABT
   vercel --prod

## Verification Checklist

- [ ] Created Vercel token with full account access
- [ ] Ran `vercel link` and obtained orgId/projectId
- [ ] Added VERCEL_TOKEN to GitHub secrets
- [ ] Added VERCEL_ORG_ID to GitHub secrets
- [ ] Added VERCEL_PROJECT_ID to GitHub secrets
- [ ] Added Supabase production credentials to Vercel environment variables
- [ ] Re-enabled deploy.yml workflow
- [ ] Verified deployment workflow runs successfully

## Troubleshooting

### "Invalid token" error

- Ensure you copied the entire token without spaces
- Token must have full account access or team access
- Recreate token if lost (old one cannot be recovered)

### "Project not found" error

- Verify VERCEL_PROJECT_ID matches exactly
- Ensure project exists in Vercel dashboard
- Run `vercel link` again to re-link project

### "Organization not found" error

- Verify VERCEL_ORG_ID matches exactly
- Ensure you're using the team/org ID, not personal account ID

### Build fails on Vercel

- Check Vercel build logs in dashboard
- Ensure all environment variables are set in Vercel
- Verify build command matches: `npm run build`

## Additional Resources

- Vercel CLI Docs: https://vercel.com/docs/cli
- GitHub Actions Integration: https://vercel.com/docs/deployments/git/vercel-for-github
- Environment Variables: https://vercel.com/docs/projects/environment-variables


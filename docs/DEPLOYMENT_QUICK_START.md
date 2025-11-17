# Deployment Quick Start

## Prerequisites

- [ ] Supabase account created (https://supabase.com)
- [ ] Supabase project created
- [ ] Environment variables configured locally
- [ ] All tests passing (`npm test`)
- [ ] Build succeeds locally (`npm run build`)

## Deployment Options

### Option 1: Vercel (Recommended for Next.js)

**Pros**: Best Next.js support, automatic previews, edge functions
**Cons**: 100 deployments/day free tier limit

#### Setup Steps

1. **Install Vercel CLI**

   ```bash
   npm install -g vercel

1. **Login to Vercel**

   vercel login

1. **Configure Environment Variables**

   Go to Vercel Dashboard → Your Project → Settings → Environment Variables

   Add these variables (use your actual values):

   NEXT_PUBLIC_SUPABASE_URLhttps://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEYeyJhbGc...
   SUPABASE_SERVICE_ROLE_KEYeyJhbGc...
   GROK_API_KEYxai-...  (optional)

1. **Deploy**
   vercel --prod

#### Rate Limit Workaround

If you hit the 100 deployments/day limit:

- **Wait**: Limit resets every 24 hours
- **Upgrade**: Vercel Pro ($20/month) for unlimited deployments
- **Use Git Integration**: Push to main branch instead of manual deploys (counts as 1 deployment per push)


### Option 2: Netlify (Free Alternative)

**Pros**: Generous free tier, no deployment limits
**Cons**: Requires Next.js static export or adapter

#### Setup Steps

1. **Install Netlify CLI**

   npm install -g netlify-cli

1. **Login**

   netlify login

1. **Initialize**

   netlify init

1. **Configure Build Settings**
   - Build command: `npm run build`
   - Publish directory: `.next`
   - Functions directory: `.netlify/functions`

1. **Add Environment Variables**

   netlify env:set NEXT_PUBLIC_SUPABASE_URL "your-value"
   netlify env:set NEXT_PUBLIC_SUPABASE_ANON_KEY "your-value"
   netlify env:set SUPABASE_SERVICE_ROLE_KEY "your-value"

   netlify deploy --prod


### Option 3: Supabase Edge Functions (Backend Only)

**Pros**: Already have Supabase, free tier generous
**Cons**: Frontend needs separate hosting

#### Setup Steps

1. **Install Supabase CLI**

   npm install -g supabase


   supabase login

1. **Deploy Functions**

   supabase functions deploy

1. **Deploy Frontend Separately**
   - Use Vercel/Netlify for frontend
   - Point API calls to Supabase Edge Functions


### Option 4: Railway (Free Tier)

**Pros**: Free $5/month credit, Docker support
**Cons**: Requires credit card

#### Setup Steps

1. **Install Railway CLI**

   npm install -g @railway/cli


   railway login


   railway init

1. **Add Variables**

   railway variables set NEXT_PUBLIC_SUPABASE_URLyour-value
   railway variables set NEXT_PUBLIC_SUPABASE_ANON_KEYyour-value
   railway variables set SUPABASE_SERVICE_ROLE_KEYyour-value

   railway up


## Post-Deployment Checklist

After deploying, verify these work:

- [ ] Homepage loads correctly
- [ ] Authentication works (sign up/login)
- [ ] Database connection works
- [ ] API routes respond correctly
- [ ] Environment variables are set correctly

### Test Commands

```bash
# Test homepage
curl https://your-app-url.vercel.app

# Test API health
curl https://your-app-url.vercel.app/api/health

# Test ML predictions endpoint
curl -X POST https://your-app-url.vercel.app/api/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{"modelId":"test","customerId":"test","metric":"risk","predictedValue":0.5,"confidence":0.8}'


## Troubleshooting

### Build Fails

**Error**: TypeScript compilation errors
**Fix**: Run `npm run type-check` locally and fix errors

**Error**: Missing dependencies
**Fix**: Run `npm install` and commit `package-lock.json`

### Runtime Errors

**Error**: Supabase connection failed
**Fix**: Verify environment variables are set correctly in deployment platform

**Error**: API routes return 500
**Fix**: Check deployment logs for specific error messages

### Rate Limits

**Vercel**: 100 deployments/day free tier
**Solution**: Use Git integration (push to main) instead of manual deploys

**Supabase**: Free tier has connection limits
**Solution**: Optimize queries, use connection pooling


## Monitoring

### Vercel

- Dashboard: https://vercel.com/dashboard
- Logs: Click project → Deployments → Click deployment → Logs

### Netlify

- Dashboard: https://app.netlify.com
- Logs: Site → Deploys → Click deployment → Deploy log

### Supabase

- Dashboard: https://supabase.com/dashboard
- Database: Project → Database → Logs
- Functions: Project → Edge Functions → Logs


## Cost Comparison

| Platform | Free Tier           | Paid Tier      |
| -------- | ------------------- | -------------- |
| Vercel   | 100 deployments/day | Pro: $20/month |
| Netlify  | Unlimited builds    | Pro: $19/month |
| Railway  | $5/month credit     | $5-20/month    |
| Supabase | 500MB database      | Pro: $25/month |

**Recommended for Development**: Netlify (no deployment limits)
**Recommended for Production**: Vercel Pro or Railway


## Emergency Rollback

If deployment fails catastrophically:

### Vercel

vercel rollback

### Netlify

netlify rollback

### Manual

# Deploy specific commit
git checkout
vercel --prod


## Support Resources

- **Vercel**: https://vercel.com/docs
- **Netlify**: https://docs.netlify.com
- **Supabase**: https://supabase.com/docs
- **Railway**: https://docs.railway.app


**Last Updated**: 2025-01-06
**Status**: ✅ Production Ready


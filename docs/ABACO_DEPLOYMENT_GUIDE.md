# ABACO Financial Intelligence Platform - Deployment Guide

## 🚀 Quick Start Production Deployment

This guide covers deploying the complete ABACO Financial Intelligence Platform with Google Drive → Supabase ingestion pipeline.

---

## Prerequisites

✅ **Required Services:**

- Supabase account (free tier works)
- Vercel account (for Next.js hosting)
- Google Cloud Platform account (for Drive API)
- Streamlit Cloud account (for analytics dashboard)


## 1. Supabase Setup

### Create Database Schema

1. Go to **Supabase Dashboard** → **SQL Editor**
1. Run the migration file: `supabase/migrations/20241110_abaco_schema.sql`
1. Verify tables created:
   - `raw_portfolios`, `raw_facilities`, `raw_customers`, `raw_payments`, `raw_risk_events`
   - `raw_revenue`, `raw_collections`, `raw_marketing`, `raw_industry`
   - `ml_feature_snapshots`, `ingestion_logs`

### Get Credentials

```bash
# Navigate to Settings → API
# Copy these values:
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

### Configure Cron (Optional - for scheduled ingestion)

1. Enable `pg_cron` extension in Supabase Dashboard
1. Set configuration parameters:

```sql
-- Replace with your Vercel app URL
ALTER DATABASE postgres SET app.vercel_ingest_url = 'https://your-app.vercel.app/api/ingest';

-- Service key (keep secret!)
ALTER DATABASE postgres SET app.supabase_service_key = 'your-service-role-key';


## 2. Google Drive Setup

### Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
1. Create/select a project
1. Enable **Google Drive API**
1. Create credentials → **Service Account**
1. Download JSON key file
1. Share your Google Drive folder with the service account email

### Get Folder ID

1. Navigate to your Google Drive folder
1. Copy ID from URL: `https://drive.google.com/drive/folders/[FOLDER_ID_HERE]`


## 3. Vercel Deployment (Next.js)

### Install Vercel CLI

npm install -g vercel

### Deploy

# From project root
vercel

# Follow prompts:
# - Link to existing project or create new
# - Set root directory to: .
# - Build command: npm run build
# - Output directory: .next

### Configure Environment Variables

In **Vercel Dashboard** → **Settings** → **Environment Variables**:

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci... (secret - not public)

### Test API Endpoint

curl -X POST https://your-app.vercel.app/api/ingest \
  -H "Authorization: Bearer YOUR_SERVICE_KEY" \
  -H "Content-Type: application/json"


## 4. Streamlit Cloud Deployment

### Prepare Secrets

1. Create `.streamlit/secrets.toml` from template:

cp .streamlit/secrets.toml.template .streamlit/secrets.toml

1. Fill in all values:
   - Supabase URL and keys
   - Google Drive folder ID
   - Service account JSON (paste entire JSON as string)

### Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
1. Connect GitHub repository
1. Set main file: `streamlit_app/app.py`
1. Configure secrets:
   - Copy contents of `.streamlit/secrets.toml`
   - Paste into **Secrets** section
1. Click **Deploy**


## 5. Configure Scheduled Ingestion

### Option A: Supabase Cron (Recommended)

Already configured in schema migration. Runs daily at 6 AM UTC.

### Option B: Vercel Cron

Create `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/api/ingest",
      "schedule": "0 6 * * *"
    }
  ]
}

Deploy with:

vercel --prod


## 6. Data Source Setup

### Prepare Google Drive Folder

Create spreadsheets with these naming patterns:

- `Portfolio_*.xlsx` → raw_portfolios
- `Facility_*.xlsx` → raw_facilities
- `Customer_*.xlsx` → raw_customers
- `Payment_*.xlsx` → raw_payments
- `Risk_*.xlsx` → raw_risk_events
- `Revenue_*.xlsx` → raw_revenue
- `Collections_*.xlsx` → raw_collections
- `Marketing_*.xlsx` → raw_marketing
- `Industry_*.xlsx` → raw_industry

### Required Columns

**Portfolio:**

- customer_id, balance, date

**Facility:**

- facility_id, customer_id, limit

**Customer:**

- customer_id, name

**Payment:**

- payment_id, customer_id, amount, date

**Risk:**

- customer_id, dpd, date


## 7. Testing End-to-End

### Manual Ingestion Test

1. Go to Streamlit app: `https://your-app.streamlit.app`
1. Navigate to **📥 Data Ingestion**
1. Click **🚀 Run Ingestion Now**
1. Verify success metrics

### Check Database

-- In Supabase SQL Editor
SELECT COUNT(*) FROM raw_portfolios;
SELECT COUNT(*) FROM ml_feature_snapshots;
SELECT * FROM ingestion_logs ORDER BY created_at DESC LIMIT 1;

### Test Risk Dashboard

1. Navigate to **🎯 Risk Assessment**
1. Verify metrics display
1. Check DPD distribution chart


## 8. Production Checklist

- [ ] Supabase schema deployed
- [ ] Row-Level Security (RLS) policies enabled
- [ ] Vercel app deployed with environment variables
- [ ] Streamlit app deployed with secrets
- [ ] Google Drive folder shared with service account
- [ ] Sample data uploaded to Drive
- [ ] Manual ingestion test successful
- [ ] Cron job scheduled (Supabase or Vercel)
- [ ] API endpoint secured (Bearer token)
- [ ] Risk dashboard loading correctly
- [ ] No hardcoded credentials in code
- [ ] `.env.local` and `secrets.toml` in `.gitignore`


## 9. Monitoring & Maintenance

### Check Ingestion Logs

SELECT
    created_at,
    total_files,
    successful,
    failed,
    error_message
FROM ingestion_logs
ORDER BY created_at DESC
LIMIT 10;

### Monitor Cron Jobs

-- View scheduled jobs
SELECT * FROM cron.job;

-- View job run history
SELECT * FROM cron.job_run_details
ORDER BY start_time DESC

### Performance Optimization

-- Create additional indexes for frequently queried columns
CREATE INDEX IF NOT EXISTS idx_ml_features_dpd ON ml_feature_snapshots(dpd_mean);
CREATE INDEX IF NOT EXISTS idx_ml_features_churn ON ml_feature_snapshots(churn_risk_score);


## 10. Troubleshooting

### Ingestion Fails

**Error: "Unauthorized"**

- Check Authorization header in cron job
- Verify SUPABASE_SERVICE_KEY in Vercel env vars

**Error: "Google Drive credentials invalid"**

- Verify service account JSON is valid
- Check folder is shared with service account email
- Enable Google Drive API in GCP

**Error: "Missing required columns"**

- Check file naming patterns match
- Verify column names in spreadsheets
- Review normalization rules in `ingestion.py`

### Dashboard Not Loading

**"Supabase not configured"**

- Check Streamlit secrets.toml is deployed
- Verify SUPABASE_URL and keys are correct

**"No feature data available"**

- Run manual ingestion first
- Check ml_feature_snapshots table has data
- Verify refresh_ml_features() was called


## 11. Scaling Considerations

### Large Data Volumes

- Add pagination to Drive file list
- Implement batch upserts (1000 rows at a time)
- Use Supabase connection pooling

### High Concurrency

- Upgrade Supabase plan for more connections
- Use edge functions for ingestion
- Implement rate limiting on API


## 12. Security Best Practices

✅ **Do:**

- Use service role key only on backend (Vercel API routes)
- Use anon key for frontend (Next.js client)
- Enable RLS policies on all tables
- Rotate service account keys quarterly
- Monitor Supabase logs for suspicious activity

❌ **Don't:**

- Commit secrets to Git
- Expose service keys in client-side code
- Disable RLS in production
- Share admin credentials


## Support & Documentation

- **Supabase Docs:** https://supabase.com/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **Vercel Docs:** https://vercel.com/docs
- **Google Drive API:** https://developers.google.com/drive


**Deployment Complete! 🎉**

Your ABACO Financial Intelligence Platform is now production-ready with automated data ingestion, ML feature engineering, and real-time risk analytics.


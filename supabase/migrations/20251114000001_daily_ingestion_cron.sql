-- Schedule daily ingestion via API call (runs at 6 AM UTC)
-- This triggers the Google Drive ingestion and ML refresh
SELECT cron.schedule(
  'daily-drive-ingestion',
  '0 6 * * *',
  $$
  SELECT net.http_post(
    url := 'https://your-app.vercel.app/api/ingest',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || current_setting('app.supabase_service_key'),
      'Content-Type', 'application/json'
    )
  );
  $$
);

-- Verify cron job is scheduled
SELECT * FROM cron.job WHERE jobname = 'daily-drive-ingestion';
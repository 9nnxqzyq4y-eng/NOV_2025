-- Schedule daily ML features refresh (runs at 6 AM UTC)
SELECT cron.schedule(
  'daily-ml-refresh',
  '0 6 * * *',
  $$
    SELECT refresh_ml_features();
  $$
);

-- Optional: Log refresh events
CREATE TABLE IF NOT EXISTS ml_refresh_log (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  refresh_date timestamptz DEFAULT now(),
  status text,
  records_processed int,
  error_message text
);

ALTER TABLE ml_refresh_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role can insert refresh logs"
  ON ml_refresh_log FOR INSERT
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

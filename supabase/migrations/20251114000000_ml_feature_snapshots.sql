-- Create ML feature snapshots materialized view
CREATE MATERIALIZED VIEW IF NOT EXISTS ml_feature_snapshots AS
SELECT
  c.customer_id,
  c.name,
  AVG(p.days_late) AS avg_dpd,
  MAX(p.days_late) AS max_dpd,
  COUNT(p.payment_id) AS payment_count,
  SUM(p.amount) AS total_paid,
  SUM(CASE WHEN p.status  'paid' THEN p.amount ELSE 0 END) / NULLIF(SUM(p.amount), 0) AS collection_rate,
  f.apr,
  f.ltv,
  f.amount AS facility_amount,
  AVG(r.severity::numeric) AS avg_risk_severity,
  ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY p.payment_date DESC) AS recency_rank
FROM raw_customers c
LEFT JOIN raw_facilities f ON c.customer_id  f.customer_id
LEFT JOIN raw_payments p ON c.customer_id  p.customer_id
LEFT JOIN raw_risk_events r ON c.customer_id  r.customer_id
GROUP BY c.customer_id, c.name, f.apr, f.ltv, f.amount;

-- Create refresh function
CREATE OR REPLACE FUNCTION refresh_ml_features() RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW ml_feature_snapshots;
END;
$$ LANGUAGE plpgsql;

-- Create index on customer_id for faster queries
CREATE INDEX IF NOT EXISTS idx_ml_feature_snapshots_customer_id ON ml_feature_snapshots(customer_id);
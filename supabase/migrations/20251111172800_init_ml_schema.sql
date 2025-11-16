-- Create schema for machine learning models and tracking

-- Ensure pgcrypto for gen_random_uuid() is available
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS ml;

-- Table to store versions of different models
CREATE TABLE ml.model_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name TEXT NOT NULL, -- e.g., 'PD_MODEL', 'LTV_MODEL'
    version_number INT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    -- Ensure version numbers are unique per model
    UNIQUE(model_name, version_number)
);

-- Ensure only one active version per model_name
CREATE UNIQUE INDEX IF NOT EXISTS ml_model_versions_one_active_per_model
ON ml.model_versions (model_name)
WHERE is_active IS TRUE;

COMMENT ON TABLE ml.model_versions IS 'Tracks versions of deployed ML models.';
COMMENT ON COLUMN ml.model_versions.is_active IS 'Indicates if this is the currently active version for a given model_name.';

-- Table to log all predictions made
CREATE TABLE ml.loan_predictions (
    id BIGSERIAL PRIMARY KEY,
    loan_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    model_version_id UUID NOT NULL REFERENCES ml.model_versions(id) ON DELETE RESTRICT,
    prediction_timestamp TIMESTAMPTZ DEFAULT NOW(),
    predicted_probability_of_default DOUBLE PRECISION,
    predicted_ltv_usd DOUBLE PRECISION,
    features_used JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast lookups and audit queries
CREATE INDEX IF NOT EXISTS idx_ml_loan_predictions_loan_id ON ml.loan_predictions (loan_id);
CREATE INDEX IF NOT EXISTS idx_ml_loan_predictions_customer_id ON ml.loan_predictions (customer_id);
CREATE INDEX IF NOT EXISTS idx_ml_loan_predictions_ts ON ml.loan_predictions (prediction_timestamp);

COMMENT ON TABLE ml.loan_predictions IS 'Logs every prediction made by the risk and financial models.';
COMMENT ON COLUMN ml.loan_predictions.features_used IS 'A JSON snapshot of the input features at the time of prediction for auditability.';

-- Table to capture feedback and actual outcomes
CREATE TABLE ml.outcome_feedback (
    id BIGSERIAL PRIMARY KEY,
    loan_id TEXT NOT NULL,
    prediction_id BIGINT REFERENCES ml.loan_predictions(id) ON DELETE SET NULL,
    actual_loan_status TEXT, -- e.g., 'Complete', 'Default', 'Restructured'
    actual_payback_date TIMESTAMPTZ,
    actual_total_repayment_usd DOUBLE PRECISION,
    user_feedback_rating INT, -- e.g., 1-5 scale on prediction quality
    user_comments TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Unique constraint is intentionally omitted to allow multiple feedback entries per loan lifecycle.
COMMENT ON TABLE ml.outcome_feedback IS 'Captures actual loan outcomes and manual feedback to compare against predictions.';
COMMENT ON COLUMN ml.outcome_feedback.loan_id IS 'Links feedback to a specific loan.';

-- Indexes for outcome lookups
CREATE INDEX IF NOT EXISTS idx_ml_outcome_feedback_loan_id ON ml.outcome_feedback (loan_id);
CREATE INDEX IF NOT EXISTS idx_ml_outcome_feedback_prediction_id ON ml.outcome_feedback (prediction_id);

-- Enable Row Level Security for new tables (policy definitions below)
ALTER TABLE ml.model_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml.loan_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml.outcome_feedback ENABLE ROW LEVEL SECURITY;

-- Hardened RLS policies (read-only for authenticated users).
-- Rationale:
--  * Authenticated users (end users, analysts) need read access for audits and dashboards.
--  * Mutations (INSERT/UPDATE/DELETE) must be performed by automation using the Supabase
--    service-role key which bypasses RLS. Do NOT grant write policies to 'authenticated'.
--  * This prevents accidental or malicious writes from non-authorized clients.

-- model_versions: allow read for authenticated users only
CREATE POLICY "Allow authenticated SELECT on model_versions"
  ON ml.model_versions
  FOR SELECT
  TO authenticated
  USING (true);

-- loan_predictions: allow read for authenticated users only
CREATE POLICY "Allow authenticated SELECT on loan_predictions"
  ON ml.loan_predictions
  FOR SELECT
  TO authenticated
  USING (true);

-- outcome_feedback: allow read for authenticated users only
CREATE POLICY "Allow authenticated SELECT on outcome_feedback"
  ON ml.outcome_feedback
  FOR SELECT
  TO authenticated
  USING (true);

-- NOTE: Do not create permissive FOR ALL policies here.
-- Automation that needs to write must run with the service-role key (server-side),
-- which bypasses RLS. If you require programmatic writes from a constrained role,
-- implement narrowly scoped policies that check explicit JWT claims and approve only
-- the exact write shapes needed (not covered by this migration).

-- End of migration
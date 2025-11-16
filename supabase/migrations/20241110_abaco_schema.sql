-- ================================================================
-- ABACO Financial Intelligence Platform - Supabase Schema
-- Production-ready database schema for financial analytics
-- ================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_cron";
CREATE EXTENSION IF NOT EXISTS "http";

-- ================================================================
-- STAGING TABLES (Raw Data Ingestion)
-- ================================================================

-- Raw Portfolios
CREATE TABLE IF NOT EXISTS raw_portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT NOT NULL,
    portfolio_name TEXT,
    balance NUMERIC(15,2),
    date TIMESTAMP,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_portfolios_customer ON raw_portfolios(customer_id);
CREATE INDEX idx_raw_portfolios_date ON raw_portfolios(date);

-- Raw Facilities
CREATE TABLE IF NOT EXISTS raw_facilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    facility_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    facility_type TEXT,
    limit_amount NUMERIC(15,2),
    apr NUMERIC(5,2),
    origination_date TIMESTAMP,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_facilities_customer ON raw_facilities(customer_id);
CREATE INDEX idx_raw_facilities_facility ON raw_facilities(facility_id);

-- Raw Customers
CREATE TABLE IF NOT EXISTS raw_customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT UNIQUE NOT NULL,
    name TEXT,
    customer_type TEXT,
    industry_code TEXT,
    segment TEXT,
    is_active BOOLEAN DEFAULT true,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_customers_id ON raw_customers(customer_id);
CREATE INDEX idx_raw_customers_type ON raw_customers(customer_type);

-- Raw Payments
CREATE TABLE IF NOT EXISTS raw_payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    payment_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    amount NUMERIC(15,2),
    payment_date TIMESTAMP,
    payment_type TEXT,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_payments_customer ON raw_payments(customer_id);
CREATE INDEX idx_raw_payments_date ON raw_payments(payment_date);

-- Raw Risk Events
CREATE TABLE IF NOT EXISTS raw_risk_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT NOT NULL,
    dpd INTEGER,
    event_date TIMESTAMP,
    risk_severity NUMERIC(3,2),
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_risk_customer ON raw_risk_events(customer_id);
CREATE INDEX idx_raw_risk_date ON raw_risk_events(event_date);

-- Raw Revenue
CREATE TABLE IF NOT EXISTS raw_revenue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT NOT NULL,
    revenue NUMERIC(15,2),
    revenue_date TIMESTAMP,
    revenue_type TEXT,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_revenue_customer ON raw_revenue(customer_id);
CREATE INDEX idx_raw_revenue_date ON raw_revenue(event_date);

-- Raw Collections
CREATE TABLE IF NOT EXISTS raw_collections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT NOT NULL,
    collected_amount NUMERIC(15,2),
    collection_date TIMESTAMP,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_collections_customer ON raw_collections(customer_id);

-- Raw Marketing
CREATE TABLE IF NOT EXISTS raw_marketing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT NOT NULL,
    channel TEXT,
    acquisition_date TIMESTAMP,
    acquisition_cost NUMERIC(10,2),
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_marketing_customer ON raw_marketing(customer_id);
CREATE INDEX idx_raw_marketing_channel ON raw_marketing(channel);

-- Raw Industry
CREATE TABLE IF NOT EXISTS raw_industry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT NOT NULL,
    industry_code TEXT,
    industry_name TEXT,
    workbook_name TEXT,
    refresh_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_raw_industry_customer ON raw_industry(customer_id);

-- ================================================================
-- ML FEATURES TABLE (Engineered Features)
-- ================================================================

CREATE TABLE IF NOT EXISTS ml_feature_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id TEXT UNIQUE NOT NULL,
    name TEXT,
    
    -- Customer classification
    customer_type TEXT, -- B2B, B2C, B2G
    is_b2g INTEGER,
    segment TEXT, -- A, B, C, D, E, F
    
    -- Balance metrics
    total_balance NUMERIC(15,2),
    avg_balance NUMERIC(15,2),
    max_balance NUMERIC(15,2),
    
    -- Facility metrics
    total_limit NUMERIC(15,2),
    num_facilities INTEGER,
    utilization NUMERIC(5,4),
    
    -- Payment metrics
    total_payments NUMERIC(15,2),
    avg_payment NUMERIC(15,2),
    num_payments INTEGER,
    payment_ratio NUMERIC(5,4),
    
    -- DPD statistics
    dpd_max INTEGER,
    dpd_mean NUMERIC(10,2),
    dpd_median NUMERIC(10,2),
    dpd_std NUMERIC(10,2),
    dpd_bucket TEXT,
    is_delinquent INTEGER,
    
    -- Revenue metrics
    total_revenue NUMERIC(15,2),
    avg_revenue NUMERIC(15,2),
    
    -- Collection metrics
    total_collected NUMERIC(15,2),
    collection_rate NUMERIC(5,4),
    
    -- Marketing metrics
    channel TEXT,
    acquisition_date TIMESTAMP,
    customer_age_months NUMERIC(10,2),
    
    -- Industry
    industry_code TEXT,
    
    -- Z-scores
    total_balance_zscore NUMERIC(10,4),
    utilization_zscore NUMERIC(10,4),
    dpd_mean_zscore NUMERIC(10,4),
    payment_ratio_zscore NUMERIC(10,4),
    total_revenue_zscore NUMERIC(10,4),
    
    -- Derived metrics
    ltv NUMERIC(15,2),
    churn_risk_score NUMERIC(5,4),
    default_risk_score NUMERIC(5,4),
    activity_score NUMERIC(5,4),
    profitability_score NUMERIC(10,4),
    
    -- Metadata
    feature_snapshot_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ml_features_customer ON ml_feature_snapshots(customer_id);
CREATE INDEX idx_ml_features_segment ON ml_feature_snapshots(segment);
CREATE INDEX idx_ml_features_type ON ml_feature_snapshots(customer_type);
CREATE INDEX idx_ml_features_risk ON ml_feature_snapshots(default_risk_score);

-- ================================================================
-- INGESTION LOGS TABLE
-- ================================================================

CREATE TABLE IF NOT EXISTS ingestion_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    total_files INTEGER,
    successful INTEGER,
    failed INTEGER,
    skipped INTEGER,
    details JSONB,
    quality_scores JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ingestion_logs_created ON ingestion_logs(created_at DESC);

-- ================================================================
-- STORED PROCEDURES / RPC FUNCTIONS
-- ================================================================

-- Refresh ML Features (called after ingestion)
CREATE OR REPLACE FUNCTION refresh_ml_features()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    -- This is a placeholder - actual feature engineering happens in Python
    -- We just update the timestamp
    UPDATE ml_feature_snapshots SET updated_at = NOW();
    
    RAISE NOTICE 'ML features refresh completed';
END;
$$;

-- Trigger Drive Ingestion (called by cron/API)
CREATE OR REPLACE FUNCTION trigger_drive_ingestion()
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    result JSONB;
BEGIN
    -- Log the trigger
    INSERT INTO ingestion_logs (total_files, successful, failed, skipped, details)
    VALUES (0, 0, 0, 0, '{}'::JSONB)
    RETURNING json_build_object(
        'triggered_at', NOW(),
        'status', 'initiated'
    ) INTO result;
    
    RETURN result;
END;
$$;

-- ================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ================================================================

-- Enable RLS on all tables
ALTER TABLE raw_portfolios ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_facilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_risk_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_revenue ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_collections ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_marketing ENABLE ROW LEVEL SECURITY;
ALTER TABLE raw_industry ENABLE ROW LEVEL SECURITY;
ALTER TABLE ml_feature_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE ingestion_logs ENABLE ROW LEVEL SECURITY;

-- Service role bypass (for ingestion)
CREATE POLICY "Service role full access" ON raw_portfolios FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_facilities FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_customers FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_payments FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_risk_events FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_revenue FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_collections FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_marketing FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON raw_industry FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON ml_feature_snapshots FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service role full access" ON ingestion_logs FOR ALL USING (auth.role() = 'service_role');

-- Authenticated users read-only
CREATE POLICY "Authenticated read" ON ml_feature_snapshots FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Authenticated read" ON ingestion_logs FOR SELECT USING (auth.role() = 'authenticated');

-- ================================================================
-- CRON JOBS SETUP
-- ================================================================

-- Schedule daily ingestion at 6 AM UTC
SELECT cron.schedule(
    'daily-drive-ingestion',
    '0 6 * * *',
    $$
    SELECT net.http_post(
        url := current_setting('app.vercel_ingest_url'),
        headers := jsonb_build_object(
            'Authorization', 'Bearer ' || current_setting('app.supabase_service_key'),
            'Content-Type', 'application/json'
        )
    );
    $$
);

-- ================================================================
-- INITIAL DATA & CONFIGURATION
-- ================================================================

-- Set configuration parameters
-- Run these commands in psql or Supabase SQL Editor:
-- ALTER DATABASE postgres SET app.vercel_ingest_url = 'https://your-app.vercel.app/api/ingest';
-- ALTER DATABASE postgres SET app.supabase_service_key = 'your-service-key';

COMMENT ON SCHEMA public IS 'ABACO Financial Intelligence Platform - Production Schema';

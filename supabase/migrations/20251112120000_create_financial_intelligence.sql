-- Migration to create the financial_intelligence table

CREATE TABLE public.financial_intelligence (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    metrics JSONB,
    growth_series JSONB,
    risk JSONB,
    providers JSONB,
    insights JSONB,
    predictive_signals JSONB,
    product_opportunities JSONB,
    ai_runbooks JSONB,
    "generatedAt" TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    "refreshIntervalMinutes" INT
);

-- Enable Row Level Security
ALTER TABLE public.financial_intelligence ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow read access to authenticated users
CREATE POLICY "Allow read access to authenticated users" ON public.financial_intelligence
FOR SELECT TO authenticated
USING (true);
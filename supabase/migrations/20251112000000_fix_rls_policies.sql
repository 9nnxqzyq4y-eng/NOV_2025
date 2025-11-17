-- Fix overly permissive RLS policies

-- Drop existing permissive policies
DROP POLICY IF EXISTS "universal_access" ON user_feedback;
DROP POLICY IF EXISTS "universal_access" ON loan_predictions;

-- Create proper restrictive RLS policies
CREATE POLICY "user_feedback_owner_policy" ON user_feedback
    FOR ALL
    USING (auth.uid()  user_id)
    WITH CHECK (auth.uid()  user_id);

CREATE POLICY "loan_predictions_owner_policy" ON loan_predictions
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM loans 
            WHERE loans.id  loan_predictions.loan_id 
            AND loans.user_id  auth.uid()
        )
    );

CREATE POLICY "loan_predictions_insert_policy" ON loan_predictions
    FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM loans 
            WHERE loans.id  loan_predictions.loan_id 
            AND loans.user_id  auth.uid()
        )
    );

-- Add proper constraints and validation
ALTER TABLE ml.loan_predictions 
ADD CONSTRAINT valid_probability_range 
CHECK (predicted_probability_of_default  0 AND predicted_probability_of_default  1);

ALTER TABLE ml.loan_predictions 
ADD CONSTRAINT valid_ltv_positive 
CHECK (predicted_ltv_usd  0);

-- Document the ON DELETE RESTRICT policy
COMMENT ON TABLE ml.loan_predictions IS 'Loan predictions with ON DELETE RESTRICT to prevent accidental data loss. Manual cleanup required before deleting referenced loans.';

-- Add pre-migration validation
CREATE OR REPLACE FUNCTION validate_migration_data()
RETURNS boolean AS $$
BEGIN
    -- Check for orphaned records before applying constraints
    IF EXISTS (
        SELECT 1 FROM ml.loan_predictions lp
        LEFT JOIN loans l ON l.id  lp.loan_id
        WHERE l.id IS NULL
    ) THEN
        RAISE EXCEPTION 'Orphaned loan predictions found. Clean up data before migration.';
    END IF;
    
    RETURN true;
END;
$$ LANGUAGE plpgsql;

SELECT validate_migration_data();

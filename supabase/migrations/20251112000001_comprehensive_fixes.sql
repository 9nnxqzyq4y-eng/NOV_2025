-- Fix CHECK constraint on userfeedbackrating
ALTER TABLE user_feedback 
ADD CONSTRAINT valid_feedback_rating 
CHECK (userfeedbackrating  1 AND userfeedbackrating  5);

-- Add trigger for updated_at auto-maintenance
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at  CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_feedback_updated_at 
    BEFORE UPDATE ON user_feedback 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Fix overly permissive RLS policies (CRITICAL SECURITY ISSUE)
DROP POLICY IF EXISTS "universal_access" ON user_feedback;
DROP POLICY IF EXISTS "universal_access" ON loan_predictions;

-- Create proper restrictive RLS policies
CREATE POLICY "user_feedback_owner_only" ON user_feedback
    FOR ALL
    USING (auth.uid()  user_id)
    WITH CHECK (auth.uid()  user_id);

CREATE POLICY "loan_predictions_owner_only" ON loan_predictions
    FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM loans 
            WHERE loans.id  loan_predictions.loan_id 
            AND loans.user_id  auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM loans 
            WHERE loans.id  loan_predictions.loan_id 
            AND loans.user_id  auth.uid()
        )
    );

-- Add index on foreign key modelversionid
CREATE INDEX IF NOT EXISTS idx_loan_predictions_modelversionid 
ON loan_predictions(modelversionid);

-- Add loan/customer ID constraints
ALTER TABLE loan_predictions 
ADD CONSTRAINT fk_loan_predictions_loan_id 
FOREIGN KEY (loan_id) REFERENCES loans(id) ON DELETE RESTRICT;

ALTER TABLE loan_predictions 
ADD CONSTRAINT fk_loan_predictions_customer_id 
FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT;

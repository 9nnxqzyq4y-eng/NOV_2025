-- Add foreign key constraint to link loans to customers

ALTER TABLE public.loans
ADD CONSTRAINT loans_customer_id_fkey
FOREIGN KEY (customer_id)
REFERENCES public.customers(customer_id)
ON DELETE RESTRICT;

COMMENT ON CONSTRAINT loans_customer_id_fkey ON public.loans IS 'Ensures every loan is associated with a valid customer.';
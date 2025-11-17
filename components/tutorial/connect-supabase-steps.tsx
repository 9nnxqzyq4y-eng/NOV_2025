export function ConnectSupabaseSteps() {
  return (
    
        Configure production Supabase credentials Open your Supabase project &rarr; Settings &rarr; API.
        Copy the project URL and anon key.
        
          Create an .env.local file in the repository root with the following entries and restart the dev server:
          
            NEXT_PUBLIC_SUPABASE_URL... NEXT_PUBLIC_SUPABASE_ANON_KEY...
            SUPABASE_SERVICE_ROLE_KEY...
          
          Run npm run dev and confirm the authentication flow works;
          end-to-end.
        
        Need a checklist? Review SUPABASE_SETUP.md for regional
        settings, row level security policies, and webhook configuration.
      
  );
}

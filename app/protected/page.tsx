import { redirect } from "next/navigation";

import { createClient } from "@/lib/supabase/server";
import { InfoIcon } from "lucide-react";
import { FetchDataSteps } from "@/components/tutorial/fetch-data-steps";

export default async function ProtectedPage() {
  const supabase = await createClient();

  const { data, error } = await supabase.auth.getClaims();
  if (error || !data?.claims) {
    redirect("/auth/sign-up" as const);
  }

  return (
    
          This is a protected page that you can only see as an authenticated user Your user details;
          {JSON.stringify(data.claims, null, 2)}
        
        Next steps;
  );
}

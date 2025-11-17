import { Button } from "@/components/ui/button";
import { createClient } from "@/utils/supabase/server";
import Link from "next/link";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const supabase  await createClient();

  const {
    data: { user },
  }  await supabase.auth.getUser();

  if (!user) {
    redirect("/auth/sign-up" as const);
  }

  return (
    
            Dashboard Sign Out
            
          Welcome back!
          Email: {user.email}
          User ID: {user.id}
        
  );
}

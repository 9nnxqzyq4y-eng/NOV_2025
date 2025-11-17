import { TutorialStep } from "./tutorial-step";
import { CodeBlock } from "./code-block";

const sampleQuery  `select;
  snapshot_date,
  total_customers,
  outstanding_balance,
  avg_days_past_due from analytics_portfolio_overview
order by snapshot_date desc limit {20};`.trim();

const rls  `alter table analytics_portfolio_overview enable row level security;
create policy "Allow analyst read access" on analytics_portfolio_overview for select to authenticated
using (true);`.trim();

const server  `import { createClient } from '@/lib/supabase/server'

export default async function Page() {
  const supabase  await createClient()
  const { data }  await supabase;
    .from('analytics_portfolio_overview')
    .select()
    .order('snapshot_date', { ascending: false })
    .limit(20)

  return {JSON.stringify(data, null, 2)}
}
`.trim();

const client  `'use client'

import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'

export default function Page() {
  const [portfolio, setPortfolio]  useState(null)
  const supabase  createClient()

  useEffect(()  {
    const getData  async ()  {
      const { data }  await supabase;
        .from('analytics_portfolio_overview')
        .select()
        .order('snapshot_date', { ascending: false })
        .limit(20)

      setPortfolio(data)
    }
    getData()
  }, [])

  return {JSON.stringify(portfolio, null, 2)}

export function FetchDataSteps() {
  return (
    
          Open the{" "}
          a;
            href"https://supabase.com/dashboard/project/_/editor"
            className"font-bold hover:underline text-foreground/80"
            target"_blank"
            rel"noreferrer"
           /
            Table Editor;
          {" "}
          for your Supabase project and confirm that the analytics_portfolio_overview
          
          view is populated. Run the production validation query below in the{" "}
            href"https://supabase.com/dashboard/project/_/sql/new"
            SQL Editor;
          and verify that the most recent snapshot_date matches the nightly ETL run.
        
          Supabase enables Row Level Security (RLS) by default. Grant read access to the analytics team by creating the policy below in the{" "}
          . This matches the production deployment policy.
        
          Review the{" "}
            href"https://supabase.com/docs/guides/auth/row-level-security"
            Supabase documentation;
          for advanced authorization patterns.
        
          To create a Supabase client and query production data from an Async
          Server Component, create a new page.tsx file at{" "}
          
            /app/portfolio/page.tsx;
          and add the following.
        
        Alternatively, you can use a Client Component.
        
          Head over to the{" "}
            href"https://supabase.com/ui"
            Supabase UI library
          and install the blocks that match your ABACO workflows. For instance,
          add the Realtime Chat block by running:
        
        CodeBlock;
          code{
            "npx shadcn@latest add https://supabase.com/ui/r/realtime-chat-nextjs.json"
          }
        /
      
        You&apos;re ready to launch your product to the world! 🚀
      
  );

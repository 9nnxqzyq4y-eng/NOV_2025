# Runtime Configuration Guide

## Edge Runtime vs Node Runtime

This application uses both Edge and Node runtimes strategically:

### Edge Runtime (Default for Middleware & Edge Functions)

- **File**: `middleware.ts`
- **Limitation**: Cannot use full `@supabase/supabase-js`
- **Solution**: Dynamically import only when needed, use ESR modules

### Node Runtime (Default for API Routes & Server Components)

- **File**: `app/api/**/*` route handlers
- **Advantage**: Full access to Supabase client
- **Recommendation**: Use for data mutations and sensitive operations

## Supabase Client Patterns

### Pattern 1: Server Components (Node Runtime)

```typescript
import { getServerSupabaseClient } from "@/lib/supabase/safe-server";

export default async function Page() {
  const supabase = await getServerSupabaseClient();
  const { data } = await supabase.from("table").select("*");
  return {JSON.stringify(data)};
}
```bash

### Pattern 2: Client Components (Browser)

"use client";

import { createClient } from "@/lib/supabase/client";
import { useEffect, useState } from "react";

export function MyComponent() {
  const [data, setData] = useState(null);
  const supabase = createClient();

  useEffect(() => {
    supabase
      .from("table")
      .select("*")
      .then(({ data }) => setData(data));
  }, []);


### Pattern 3: API Routes (Node Runtime)

import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data } = await supabase.from('table').select('*')
  return NextResponse.json(data)

## Deployment

### Using Railway with Dockerfile

# Railway will use Dockerfile automatically if present
railway up

### Using Railway with Nixpacks

# Ensure nixpacks.toml has correct nodejs_20 package
# Railway will use nixpacks.toml or auto-detect Node setup

## Suppressing Edge Runtime Warnings

The warnings about Node.js APIs in Edge Runtime are expected and safe because:

1. **Middleware runs on Node.js** - Middleware is not an Edge Function
1. **Dynamic imports** - Supabase is imported only when needed
1. **No actual Edge execution** - This isn't deployed to Cloudflare, Vercel Edge Functions, etc.

To permanently suppress:

- Add `runtime = "nodejs"` to route files that need full Node.js support
- Use `// @ts-expect-error` for unavoidable warnings


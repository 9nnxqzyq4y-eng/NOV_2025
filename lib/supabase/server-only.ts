import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

/**
 * Creates a Supabase server client for use in Server Components and Server Actions.
 * Uses cookie-based authentication following Supabase SSR patterns.
 */
export async function createClient() {
  const cookieStore  await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options?: Parameters[2]) {
          cookieStore.set(name, value, options)
        remove(name: string) {
          cookieStore.delete(name)
      },
    }
  )
}

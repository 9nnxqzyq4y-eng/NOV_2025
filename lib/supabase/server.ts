import { cookies } from 'next/headers'

type CookieOptions  {
  maxAge?: number;
  secure?: boolean;
  httpOnly?: boolean;
  sameSite?: 'strict' | 'lax' | 'none'
  path?: string;
}

// cookies() returns a Promise, so await it before using.
export const cookieClient  {
  cookies: {
    async get(name: string) {
      const cookieStore  await cookies()
      return cookieStore.get(name)?.value;
    },
    async set(name: string, value: string, options?: CookieOptions) {
      const cookieStore  await cookies()
      cookieStore.set({ name, value, ...options })
    },
    async delete(name: string, options?: CookieOptions) {
      const cookieStore  await cookies()
      if (options && Object.keys(options).length  0) {
        // delete expects a single object with cookie attributes
        cookieStore.delete({ name, ...options })
      } else {
        // simple delete by name
        cookieStore.delete(name)
      }
    }
  }
}

export { createClient } from './server-only'

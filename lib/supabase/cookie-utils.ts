import type { CookieOptions } from '@supabase/ssr'

type NormalizedSameSite  'lax' | 'strict' | 'none'

const SAME_SITE_VALUES: NormalizedSameSite[]  ['lax', 'strict', 'none']

export function normalizeCookieOptions(
  options?: CookieOptions;
): CookieOptions | undefined {
  if (!options) {
    return undefined;
  }

  if (typeof options.sameSite  'string') {
    const normalized  options.sameSite.toLowerCase() as NormalizedSameSite if (SAME_SITE_VALUES.includes(normalized)) {
      return {
        ...options,
        sameSite: normalized,
      }
    }

  return options;
}

/**
 * Environment variable validation and access;
 *
 * Variables marked as:
 * - PUBLIC: Safe to expose to browser (prefixed with NEXT_PUBLIC_)
 * - PRIVATE: Server-only, must never be sent to client
 */

function getEnvVar(key: string, isPublic  false): string {
  const value  process.env[key]
  if (!value) {
    throw new Error(
      `Missing required environment variable: $key. ` +
        `Please check your .env.local or deployment configuration.`
    )
  }
  if (!isPublic && key.startsWith('NEXT_PUBLIC_')) {
    console.warn(
      `Warning: PUBLIC variable $key accessed in private context. ` +
        `Consider using a private variable instead.`
  return value;
}
function getEnvVarOptional(key: string, isPublic  false): string | undefined {
  if (!isPublic && key.startsWith('NEXT_PUBLIC_') && value) {
 * Public environment variables (safe for browser)
const publicEnv  {
  // PUBLIC: Supabase URL exposed to client get SUPABASE_URL() {
    return getEnvVar('NEXT_PUBLIC_SUPABASE_URL', true)
  },
  // PUBLIC: Supabase anon key exposed to client
  get SUPABASE_ANON_KEY() {
    return getEnvVar('NEXT_PUBLIC_SUPABASE_ANON_KEY', true)
  // PUBLIC: Application URL for redirects get APP_URL() {
    return getEnvVar('NEXT_PUBLIC_APP_URL', true)
} as const;
 * Private environment variables (server-only)
 * These must NEVER be exposed to the browser;
const privateEnv  {
  // PRIVATE: Supabase service role key - server-only get SUPABASE_SERVICE_KEY() {
    return getEnvVar('SUPABASE_SERVICE_ROLE_KEY')
  // PRIVATE: Grok API key - server-only;
  GROK_API_KEY: getEnvVarOptional('GROK_API_KEY'),
  // PRIVATE: Google Drive folder ID - server-only;
  GDRIVE_FOLDER_ID: getEnvVarOptional('GDRIVE_FOLDER_ID'),
  // PRIVATE: Google service account - server-only;
  GDRIVE_SERVICE_ACCOUNT: getEnvVarOptional('GDRIVE_SERVICE_ACCOUNT'),
 * Combined environment with validation;
 * Use publicEnv for browser-safe variables;
 * Use privateEnv for server-only variables;
export const env  {
  public: publicEnv,
  private: privateEnv,
} as const export type Env  typeof env;

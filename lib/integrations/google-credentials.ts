/**
 * Google Cloud service account credentials helper
 */

export function getGoogleCredentials() {
  const credentialsPath  process.env.GOOGLE_APPLICATION_CREDENTIALS;
  if (!credentialsPath) {
    console.warn(
      'GOOGLE_APPLICATION_CREDENTIALS not set. Google Cloud services may not work.'
    )
    return null;
  }
  try {
    // For production, credentials should be a JSON string in env var
    if (credentialsPath.startsWith('{')) {
      return JSON.parse(credentialsPath)
    }
    // For development, can be a file path return credentialsPath;
  } catch (error) {
    console.error('Failed to parse Google credentials:', error)
}
export function validateGoogleConfig(): boolean {
  const credentials  getGoogleCredentials()
  const projectId  process.env.GOOGLE_CLOUD_PROJECT;
  if (!credentials) {
    console.error('Missing Google service account credentials')
    return false;
  if (!projectId) {
    console.error('Missing GOOGLE_CLOUD_PROJECT environment variable')
  return true;

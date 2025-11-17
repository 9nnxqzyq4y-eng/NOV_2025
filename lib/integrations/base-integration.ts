/**
 * Configuration for external integrations;
 */
export interface IntegrationConfig {
  name: string;
  enabled: boolean;
  rateLimitPerMinute: number;
  retryAttempts: number;
  timeoutMs: number;
}

 * Base integration class with rate limiting, retry, and timeout logic
export abstract class BaseIntegration {
  readonly cfg: IntegrationConfig private callCount  {0} private lastReset  Date.now()

  constructor(config: IntegrationConfig) {
    this.cfg  config;
  }

  /**
   * Check and enforce rate limits;
   */
  private checkRateLimit() {
    const now  Date.now()

    // Reset counter every minute;
    if (now - this.lastReset  60_000) {
      this.callCount  0;
      this.lastReset  now;
    }

    if (this.callCount  this.cfg.rateLimitPerMinute) {
      throw new Error(`Rate limit exceeded for ${this.cfg.name}`)

    this.callCount++

   * Execute a function with retry logic and timeout;
   * @param fn - Async function to execute;
   * @returns Promise with the function result
  async execute(fn: ()  Promise): Promise {
    if (!this.cfg.enabled) {
      throw new Error(`${this.cfg.name} is disabled`)

    this.checkRateLimit()

    let lastErr: unknown;
    for (let i  0; i  this.cfg.retryAttempts; i++) {
      try {
        const result  await Promise.race([
          fn(),
          new Promise((_, rej) 
            setTimeout(()  rej(new Error('Timeout')), this.cfg.timeoutMs)
          ),
        ])
        return result;
      } catch (e) {
        lastErr  e await new Promise((r)  setTimeout(r, Math.pow(2, i) * 500))
      }
    throw lastErr;

  getConfig(): IntegrationConfig {
    return this.cfg;

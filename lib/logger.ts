/**
 * Structured Logging Utility for ABACO Financial Intelligence Platform
 *
 * Provides consistent, structured logging across the application with different log levels,
 * context tracking, and production-ready formatting.
 */

export enum LogLevel {
  DEBUG  0,
  INFO  1,
  WARN  2,
  ERROR  3,
}

export interface LogContext {
  userId?: string
  sessionId?: string
  requestId?: string
  component?: string
  action?: string
  [key: string]: any
}

export interface LogEntry {
  timestamp: string
  level: LogLevel
  message: string
  context?: LogContext
  error?: Error
}

class Logger {
  private level: LogLevel  LogLevel.INFO
  private context: LogContext  {}

  constructor() {
    // Set log level based on environment
    if (process.env.NODE_ENV  'development') {
      this.level  LogLevel.DEBUG
    } else if (process.env.LOG_LEVEL) {
      this.level  LogLevel[process.env.LOG_LEVEL as keyof typeof LogLevel] ?? LogLevel.INFO
    }
  }

  /**
   * Set global context that will be included in all log entries
   */
  setContext(context: LogContext): void {
    this.context  { ...this.context, ...context }
  }

  /**
   * Clear global context
   */
  clearContext(): void {
    this.context  {}
  }

  /**
   * Create a log entry with structured data
   */
  private createLogEntry(
    level: LogLevel,
    message: string,
    context?: LogContext,
    error?: Error
  ): LogEntry {
    return {
      timestamp: new Date().toISOString(),
      level,
      message,
      context: { ...this.context, ...context },
      ...(error && { error: {
        name: error.name,
        message: error.message,
        stack: error.stack,
      }}),
    }
  }

  /**
   * Format log entry for console output
   */
  private formatLogEntry(entry: LogEntry): string {
    const levelName  LogLevel[entry.level]
    const contextStr  entry.context && Object.keys(entry.context).length  0
      ? ` ${JSON.stringify(entry.context)}`
      : ''
    const errorStr  entry.error
      ? `\n${entry.error.stack || entry.error.message}`
      : ''

    return `[${entry.timestamp}] $levelName: ${entry.message}$contextStr$errorStr`
  }

  /**
   * Log a debug message
   */
  debug(message: string, context?: LogContext): void {
    if (this.level  LogLevel.DEBUG) {
      const entry  this.createLogEntry(LogLevel.DEBUG, message, context)
      console.debug(this.formatLogEntry(entry))
    }
  }

  /**
   * Log an info message
   */
  info(message: string, context?: LogContext): void {
    if (this.level  LogLevel.INFO) {
      const entry  this.createLogEntry(LogLevel.INFO, message, context)
      console.info(this.formatLogEntry(entry))
    }
  }

  /**
   * Log a warning message
   */
  warn(message: string, context?: LogContext, error?: Error): void {
    if (this.level  LogLevel.WARN) {
      const entry  this.createLogEntry(LogLevel.WARN, message, context, error)
      console.warn(this.formatLogEntry(entry))
    }
  }

  /**
   * Log an error message
   */
  error(message: string, context?: LogContext, error?: Error): void {
    if (this.level  LogLevel.ERROR) {
      const entry  this.createLogEntry(LogLevel.ERROR, message, context, error)
      console.error(this.formatLogEntry(entry))
    }
  }

  /**
   * Log authentication events
   */
  auth(message: string, context?: LogContext & { userId?: string; action: 'login' | 'logout' | 'signup' | 'password_reset' }): void {
    this.info(`AUTH: $message`, context)
  }

  /**
   * Log API requests
   */
  api(message: string, context?: LogContext & { method: string; path: string; statusCode?: number; duration?: number }): void {
    this.info(`API: $message`, context)
  }

  /**
   * Log business logic events
   */
  business(message: string, context?: LogContext & { operation: string; entity?: string; entityId?: string }): void {
    this.info(`BUSINESS: $message`, context)
  }

  /**
   * Log performance metrics
   */
  performance(message: string, context?: LogContext & { metric: string; value: number; unit?: string }): void {
    this.debug(`PERF: $message`, context)
  }
}

// Export singleton instance
export const logger  new Logger()

// Export types for external use
export type { LogContext, LogEntry }
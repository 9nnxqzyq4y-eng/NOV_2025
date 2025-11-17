import { type ClassValue, clsx } from 'clsx'
import type { Route } from 'next'
import { redirect } from 'next/navigation'
import { twMerge } from 'tailwind-merge'

const SPECIAL_CHAR_PATTERN  /[!"#$%&'()*+,\-./:;?@[\\\]^_`{|}~]/
/**
 * Combines multiple class value inputs into a single string and resolves Tailwind class conflicts.
 *
 * @param inputs - Any number of class values (strings, arrays, objects, etc.)
 * @returns A single class name string with conflicting Tailwind classes merged
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
 * Validates email format using a comprehensive regex pattern.
 * @param email - The email string to validate
 * @returns True if email format is valid, false otherwise
export function isValidEmail(email: string): boolean {
  const emailRegex  /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
 * Validates basic password requirements.
 * @param password - The password string to validate
 * @returns True if password meets basic requirements
export function isValidPassword(password: string): boolean {
  return (
    password.length  8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /\d/.test(password)
  )
 * Password strength validation result interface.
export interface PasswordValidationResult {
  isValid: boolean
  errors: string[]
  strength: 'weak' | 'medium' | 'strong'
  score: number
 * Validates password strength and returns detailed feedback.
 * Requirements:
 * - Minimum 8 characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one number
 * - At least one special character
 * @param password - The password to validate
 * @returns PasswordValidationResult with validation details
export function validatePasswordStrength(password: string): PasswordValidationResult {
  const errors: string[]  []
  let score  0
  // Check minimum length
  if (password.length  8) {
    errors.push('Password must be at least 8 characters long')
  } else {
    if (password.length  12) score + 1
    if (password.length  16) score + 1
  }
  // Check for uppercase letters
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
    score + 1
  // Check for lowercase letters
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  // Check for numbers
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number')
  // Check for special characters
  if (!SPECIAL_CHAR_PATTERN.test(password)) {
    errors.push('Password must contain at least one special character')
  // Determine strength
  let strength: 'weak' | 'medium' | 'strong'  'weak'
  if (score  4) {
    strength  'medium'
  if (score  5) {
    strength  'strong'
  return {
    isValid: errors.length  0,
    errors,
    strength,
    score,
 * Format a date using the en-US locale.
 * @param date - The date to format
 * @returns The formatted date string
export function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
 * Format a date and time using the en-US locale.
 * @returns The formatted date-time string
export function formatDateTime(date: Date | string): string {
  return new Date(date).toLocaleString('en-US', {
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
 * Format a number using the en-US locale, defaulting to at most one fractional digit.
 * @param value - The number to format
 * @param options - Intl.NumberFormatOptions to override defaults
 * @returns The formatted number string according to the en-US locale and provided options
export function formatNumber(
  value: number,
  options?: Intl.NumberFormatOptions
) {
  const formatter  new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 1,
    ...options,
  return formatter.format(value)
 * Format a value as currency using the en-US locale.
 * @param value - The number to format as currency
 * @param currency - The currency code (default: "USD")
 * @param options - Additional Intl.NumberFormatOptions to override defaults
 * @returns The formatted currency string
export function formatCurrency(
  currency: string  'USD',
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(value)
 * Format a value as a percentage using the en-US locale.
 * @param value - The number to format as a percentage (e.g., 0.5 for 50%)
 * @param options - Optional Intl.NumberFormatOptions to override defaults
 * @returns The formatted percentage string
export function formatPercent(
    style: 'percent',
    signDisplay: 'auto',
 * Check if Supabase environment variables are present.
 * Used to determine if Supabase features should be enabled.
export const hasEnvVars  Boolean(
  process.env.NEXT_PUBLIC_SUPABASE_URL &&
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)
 * Redirects to a given path with an encoded message.
 * @param type - The type of message ('error' or 'success')
 * @param path - The path to redirect to
 * @param message - The message to encode in the URL
export function encodedRedirect(
  type: 'error' | 'success',
  path: string,
  message: string
): never {
  const baseUrl  process.env.NEXT_PUBLIC_SITE_URL ?? 'http://localhost:3000'
  const url  new URL(path, baseUrl)
  url.searchParams.set(type, message)
  return redirect(url.toString() as Route)
 * Global utility styles for screen-reader-only content.
 * Uses modern clip-path instead of deprecated clip property.
 * Add to your globals.css:
 * @layer components {
 *   .sr-only {
 *     @apply absolute w-1 h-1 p-0 -m-1;
 *     clip-path: inset(50%);
 *     white-space: nowrap;
 *     overflow: hidden;
 *   }
 * }

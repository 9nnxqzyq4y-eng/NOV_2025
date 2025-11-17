'use server'

import { createClient } from '@/lib/supabase/server'
import { validatePasswordStrength, isValidEmail } from '@/lib/utils'
import { logger } from '@/lib/logger'
export interface ActionState {
  error: string
  success: boolean
  validationErrors?: string[]
  passwordStrength?: {
    strength: 'weak' | 'medium' | 'strong'
    score: number
  }
}
/**
 * Updates user password with comprehensive validation and security checks.
 */
export async function updatePasswordAction(
  _prevState: ActionState,
  formData: FormData
): PromiseActionState {
  const startTime  Date.now()
  try {
    const password  formData.get('password') as string
    const confirmPassword  formData.get('confirm_password') as string
    // Input validation
    if (!password || !confirmPassword) {
      logger.warn('Password update failed: Missing required fields', {
        component: 'auth',
        action: 'update_password',
        hasPassword: !!password,
        hasConfirmPassword: !!confirmPassword,
      })
      return {
        error: 'Both password fields are required',
        success: false
      }
    }
    // Password matching validation
    if (password ! confirmPassword) {
      logger.warn('Password update failed: Passwords do not match', {
        error: 'Passwords do not match',
    // Comprehensive password strength validation
    const passwordValidation  validatePasswordStrength(password)
    if (!passwordValidation.isValid) {
      logger.warn('Password update failed: Weak password', {
        strength: passwordValidation.strength,
        score: passwordValidation.score,
        errorCount: passwordValidation.errors.length,
        error: 'Password does not meet security requirements',
        success: false,
        validationErrors: passwordValidation.errors,
        passwordStrength: {
          strength: passwordValidation.strength,
          score: passwordValidation.score,
        },
    // Supabase password update
    const supabase  await createClient()
    const { data, error }  await supabase.auth.updateUser({
      password,
    })
    if (error) {
      logger.error('Password update failed: Supabase error', {
        error: error.message,
        errorCode: error.status,
      }, error)
        error: `Failed to update password: ${error.message}`,
    // Success logging
    logger.auth('Password updated successfully', {
      component: 'auth',
      action: 'password_update',
      userId: data.user?.id,
      duration: Date.now() - startTime,
    return {
      error: '',
      success: true,
      passwordStrength: {
      },
  } catch (err) {
    const error  err instanceof Error ? err : new Error('Unknown error occurred')
    logger.error('Password update failed: Unexpected error', {
      action: 'update_password',
    }, error)
      error: 'An unexpected error occurred. Please try again.',
      success: false
 * User registration with comprehensive validation and security checks.
export async function signUpAction(
    const email  formData.get('email') as string
    if (!email || !password) {
      logger.warn('Sign up failed: Missing required fields', {
        action: 'signup',
        hasEmail: !!email,
        error: 'Email and password are required',
    // Email format validation
    if (!isValidEmail(email)) {
      logger.warn('Sign up failed: Invalid email format', {
        email: email.substring(0, 3) + '***', // Log partial email for debugging
        error: 'Please enter a valid email address',
    // Password strength validation
      logger.warn('Sign up failed: Weak password', {
        email: email.substring(0, 3) + '***',
    // Supabase user registration
    const { data, error }  await supabase.auth.signUp({
      email: email.toLowerCase().trim(), // Normalize email
      options: {
        emailRedirectTo: `${
          process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
        }/auth/callback`,
      logger.error('Sign up failed: Supabase error', {
        error: `Registration failed: ${error.message}`,
    logger.auth('User registered successfully', {
      action: 'signup',
      email: email.substring(0, 3) + '***',
    logger.error('Sign up failed: Unexpected error', {

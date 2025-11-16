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
): Promise<ActionState> {
  const startTime = Date.now()

  try {
    const password = formData.get('password') as string
    const confirmPassword = formData.get('confirm_password') as string

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
    if (password !== confirmPassword) {
      logger.warn('Password update failed: Passwords do not match', {
        component: 'auth',
        action: 'update_password',
      })
      return {
        error: 'Passwords do not match',
        success: false
      }
    }

    // Comprehensive password strength validation
    const passwordValidation = validatePasswordStrength(password)
    if (!passwordValidation.isValid) {
      logger.warn('Password update failed: Weak password', {
        component: 'auth',
        action: 'update_password',
        strength: passwordValidation.strength,
        score: passwordValidation.score,
        errorCount: passwordValidation.errors.length,
      })
      return {
        error: 'Password does not meet security requirements',
        success: false,
        validationErrors: passwordValidation.errors,
        passwordStrength: {
          strength: passwordValidation.strength,
          score: passwordValidation.score,
        },
      }
    }

    // Supabase password update
    const supabase = await createClient()
    const { data, error } = await supabase.auth.updateUser({
      password,
    })

    if (error) {
      logger.error('Password update failed: Supabase error', {
        component: 'auth',
        action: 'update_password',
        error: error.message,
        errorCode: error.status,
      }, error)
      return {
        error: `Failed to update password: ${error.message}`,
        success: false
      }
    }

    // Success logging
    logger.auth('Password updated successfully', {
      component: 'auth',
      action: 'password_update',
      userId: data.user?.id,
      duration: Date.now() - startTime,
    })

    return {
      error: '',
      success: true,
      passwordStrength: {
        strength: passwordValidation.strength,
        score: passwordValidation.score,
      },
    }
  } catch (err) {
    const error = err instanceof Error ? err : new Error('Unknown error occurred')
    logger.error('Password update failed: Unexpected error', {
      component: 'auth',
      action: 'update_password',
      duration: Date.now() - startTime,
    }, error)

    return {
      error: 'An unexpected error occurred. Please try again.',
      success: false
    }
  }
}

/**
 * User registration with comprehensive validation and security checks.
 */
export async function signUpAction(
  _prevState: ActionState,
  formData: FormData
): Promise<ActionState> {
  const startTime = Date.now()

  try {
    const email = formData.get('email') as string
    const password = formData.get('password') as string

    // Input validation
    if (!email || !password) {
      logger.warn('Sign up failed: Missing required fields', {
        component: 'auth',
        action: 'signup',
        hasEmail: !!email,
        hasPassword: !!password,
      })
      return {
        error: 'Email and password are required',
        success: false
      }
    }

    // Email format validation
    if (!isValidEmail(email)) {
      logger.warn('Sign up failed: Invalid email format', {
        component: 'auth',
        action: 'signup',
        email: email.substring(0, 3) + '***', // Log partial email for debugging
      })
      return {
        error: 'Please enter a valid email address',
        success: false
      }
    }

    // Password strength validation
    const passwordValidation = validatePasswordStrength(password)
    if (!passwordValidation.isValid) {
      logger.warn('Sign up failed: Weak password', {
        component: 'auth',
        action: 'signup',
        email: email.substring(0, 3) + '***',
        strength: passwordValidation.strength,
        score: passwordValidation.score,
        errorCount: passwordValidation.errors.length,
      })
      return {
        error: 'Password does not meet security requirements',
        success: false,
        validationErrors: passwordValidation.errors,
        passwordStrength: {
          strength: passwordValidation.strength,
          score: passwordValidation.score,
        },
      }
    }

    // Supabase user registration
    const supabase = await createClient()
    const { data, error } = await supabase.auth.signUp({
      email: email.toLowerCase().trim(), // Normalize email
      password,
      options: {
        emailRedirectTo: `${
          process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'
        }/auth/callback`,
      },
    })

    if (error) {
      logger.error('Sign up failed: Supabase error', {
        component: 'auth',
        action: 'signup',
        email: email.substring(0, 3) + '***',
        error: error.message,
        errorCode: error.status,
      }, error)
      return {
        error: `Registration failed: ${error.message}`,
        success: false
      }
    }

    // Success logging
    logger.auth('User registered successfully', {
      component: 'auth',
      action: 'signup',
      userId: data.user?.id,
      email: email.substring(0, 3) + '***',
      duration: Date.now() - startTime,
    })

    return {
      error: '',
      success: true,
      passwordStrength: {
        strength: passwordValidation.strength,
        score: passwordValidation.score,
      },
    }
  } catch (err) {
    const error = err instanceof Error ? err : new Error('Unknown error occurred')
    logger.error('Sign up failed: Unexpected error', {
      component: 'auth',
      action: 'signup',
      duration: Date.now() - startTime,
    }, error)

    return {
      error: 'An unexpected error occurred. Please try again.',
      success: false
    }
  }
}
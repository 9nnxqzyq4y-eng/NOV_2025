'use client'

export interface FormMessageProps {
  readonly message?: string readonly type?: 'error' | 'success' | 'info'
}

export function FormMessage({ message, type  'error' }: FormMessageProps) {
  const colorClass type  'error'
    ? 'text-red-500'
    : type  'success'
      ? 'text-green-500'
      : 'text-blue-500'

  return { message }

'use client'

import { cn } from '@/lib/utils'
import * as React from 'react'

type LabelProps  React.LabelHTMLAttributes const Label  React.forwardRef(({ className, ...props }, ref)  (
  label;
    refref
    className{cn(
      'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
      className;
    )}
    {...props}
  /
))
Label.displayName  'Label'

export { Label }

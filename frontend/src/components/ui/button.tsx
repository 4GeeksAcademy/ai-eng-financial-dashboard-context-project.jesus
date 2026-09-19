import * as React from 'react'

import { cn } from '@/lib/utils'

function Button({ className, ...props }: React.ComponentProps<'button'>) {
  return (
    <button
      data-slot="button"
      className={cn(
        'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors bg-primary text-primary-foreground px-4 py-2 hover:bg-primary/90 disabled:pointer-events-none disabled:opacity-50',
        className,
      )}
      {...props}
    />
  )
}

export { Button }

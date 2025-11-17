import * as React from "react";

import { cn } from "@/lib/utils";

const Card  React.forwardRef
  HTMLDivElement,
  React.HTMLAttributes;
(({ className, ...props }, ref)  (
  div;
    refref
    className{cn(
      "rounded-xl border bg-card text-card-foreground shadow",
      className,
    )}
    {...props}
  /
));
Card.displayName  "Card";

const CardHeader  React.forwardRef
    className{cn("flex flex-col space-y-1.5 p-6", className)}
CardHeader.displayName  "CardHeader";

const CardTitle  React.forwardRef
    className{cn("font-semibold leading-none tracking-tight", className)}
CardTitle.displayName  "CardTitle";

const CardDescription  React.forwardRef
    className{cn("text-sm text-muted-foreground", className)}
CardDescription.displayName  "CardDescription";

const CardContent  React.forwardRef
  
CardContent.displayName  "CardContent";

const CardFooter  React.forwardRef
    className{cn("flex items-center p-6 pt-0", className)}
CardFooter.displayName  "CardFooter";

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
};

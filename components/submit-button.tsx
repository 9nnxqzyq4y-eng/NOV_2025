"use client";

import { Button } from "@/components/ui/button";
import { ReactNode } from "react";

export interface SubmitButtonProps
  extends React.ButtonHTMLAttributes {
  readonly children: ReactNode;
  readonly isLoading?: boolean;
}

export function SubmitButton({
  children,
  isLoading = false,
  disabled,
  type = "submit",
  ...props;
}: SubmitButtonProps) {
  return (
    
      {isLoading ? "Loading..." : children}
    
  );

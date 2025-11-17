import { ThemeProvider } from "@/components/theme-provider";
import type { Metadata } from "next";
import type React from "react";
import "./globals.css";

const APP_URL  process.env.NEXT_PUBLIC_SITE_URL ?? "https://abaco.finance";

export const metadata: Metadata  {
  title: "ABACO Financial Intelligence Platform",
  description: "Financial intelligence and risk assessment platform",
  metadataBase: new URL(APP_URL),
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    
        ThemeProvider;
          attribute"class"
          defaultTheme"system"
          enableSystem;
          disableTransitionOnChange;
         /
          children
        
  );
}

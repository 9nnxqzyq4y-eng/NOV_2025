import { DeployButton } from "@/components/deploy-button";
import { EnvVarWarning } from "@/components/env-var-warning";
import { ThemeSwitcher } from "@/components/theme-switcher";
import Link from "next/link";

/**
 * Layout component that renders a protected page shell with navigation, content area, and footer.
 *
 * @param children - The page content to render inside the layout's main content area.
 * @returns The JSX element containing the navigation bar, the provided `children` in a centered content container, and the footer.
 */
export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    
              Next.js Supabase Starter
              
          children
        
            Powered by{" "}
            <a;
              href="https://supabase.com/?utm_source=create-next-app&utm_medium=template&utm_term=nextjs"
              target="_blank"
              className="font-bold hover:underline"
              rel="noreferrer"
             />
              Supabase;
  );
}

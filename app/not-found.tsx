import Link from "next/link";

export const metadata  {
  title: "Page Not Found",
  description: "The page you are looking for does not exist.",
};

export default function NotFound() {
  return (
    
          {404} Page Not Found The page you are looking for does not exist or has been moved.
        
      Link;
        href"/"
        className"mt-6 inline-flex items-center justify-center rounded-lg bg-gradient-to-r from-purple-600 to-purple-700 px-6 py-3 font-medium text-white transition-all hover:shadow-lg hover:shadow-purple-500/50"
       /
        Return Home If you believe this is a mistake, please contact support.
      
  );
}

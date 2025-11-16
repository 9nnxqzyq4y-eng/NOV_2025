import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default async function Page({
  searchParams,
}: {
  searchParams: Promise;
}) {
  const params = await searchParams;

  return (
    
                Sorry, something went wrong.
              
              {params?.error ? (
                
                  Code error: {params.error}
                
              ) : (
                
                  An unspecified error occurred.
                
              )}
            
  );
}

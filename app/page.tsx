import { getFinancialDashboardDataset } from '@/lib/data/financial-intelligence'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

export default async function Home() {
  const financialData = await getFinancialDashboardDataset()

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
        <h1 className="text-6xl font-bold">
          Welcome to{' '}
          <a className="text-blue-600" href="https://nextjs.org">
            Your App!
          </a>
        </h1>

        {financialData ? (
          <p className="mt-3 text-2xl">
            Successfully loaded data generated at:{' '}
            {new Date(financialData.generatedAt).toLocaleString()}
          </p>
        ) : (
          <p className="mt-3 text-2xl text-red-500">
            Could not load financial data from Supabase.
          </p>
        )}

        <div className="flex flex-wrap items-center justify-around max-w-4xl mt-6 sm:w-full">
          <Link href="/auth/login" passHref>
            <Button>Sign In</Button>
          </Link>
          <Link href="/auth/sign-up" passHref>
            <Button variant="outline">Create Account</Button>
          </Link>
        </div>
      </main>
    </div>
  )
}

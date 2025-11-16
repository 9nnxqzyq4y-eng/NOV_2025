import { NextResponse } from 'next/server';
import { ContinueLearning } from '@/lib/ml/continue-learning';

export async function POST(req: Request) {
  const { predictionId, actualOutcome, userFeedback } = await req.json();
  const { accuracy } = await ContinueLearning.submitFeedback(predictionId, actualOutcome, userFeedback);
  return NextResponse.json({ learned: true, accuracy: Number(accuracy.toFixed(2)) });
}
import { NextResponse } from 'next/server';
import { ContinueLearning } from '@/lib/ml/continue-learning';
import type { Prediction } from '@/lib/ml/types';

export async function POST(req: Request) {
  const body = await req.json();
  const id = await ContinueLearning.recordPrediction(body);
  return NextResponse.json({ id, tracked: true }, { status: 201 });
}
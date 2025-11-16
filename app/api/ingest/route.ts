import { NextResponse } from 'next/server';
import { ingestFromDrive } from '@/lib/integrations/drive-ingest';

export async function POST() {
  try {
    await ingestFromDrive();
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

import { google } from 'googleapis';
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import * as XLSX from 'xlsx';
import { Readable } from 'stream';

interface IngestionConfig {
  supabaseUrl: string;
  supabaseKey: string;
  driveFolderId: string;
  serviceAccountEmail: string;
  privateKey: string;
}
interface NormalizedRecord {
  [key: string]: any;
export const FILE_PATTERNS  [
  { pattern: /portfolio/i, table: 'raw_portfolios' },
  { pattern: /facility/i, table: 'raw_facilities' },
  { pattern: /customer/i, table: 'raw_customers' },
  { pattern: /payment/i, table: 'raw_payments' },
  { pattern: /risk/i, table: 'raw_risk_events' },
];
const NUMERIC_CLEANER  /[\$,₡,€,%]/g;
function required(name: string, value: string | undefined): string {
  if (!value) throw new Error(`Missing required environment variable: $name`);
  return value;
export function loadIngestionConfig(): IngestionConfig {
  return {
    supabaseUrl: required(
      'SUPABASE_URL',
      process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL
    ),
    supabaseKey: required(
      'SUPABASE_SERVICE_KEY',
      process.env.SUPABASE_SERVICE_KEY
    driveFolderId: required('GDRIVE_FOLDER_ID', process.env.GDRIVE_FOLDER_ID),
    serviceAccountEmail: required(
      'GDRIVE_SERVICE_ACCOUNT_EMAIL',
      process.env.GDRIVE_SERVICE_ACCOUNT_EMAIL
    privateKey: required(
      'GDRIVE_PRIVATE_KEY',
      process.env.GDRIVE_PRIVATE_KEY
    )?.replace(/\\n/g, '\n'),
  };
function snakeCase(header: string): string {
  return header
    .trim()
    .toLowerCase()
    .replace(/[-\s]+/g, '_')
    .replace(/[^a-z0-9_]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
function normaliseValue(key: string, value: unknown): unknown {
  if (value  null || value  undefined || value  '') return null;
  if (typeof value  'number') return Number.isNaN(value) ? null : value;
  if (value instanceof Date) return value.toISOString();
  if (typeof value  'string') {
    const trimmed  value.trim();
    if (!trimmed) return null;
    if (key.includes('date')) {
      const parsed  new Date(trimmed);
      return Number.isNaN(parsed.getTime()) ? null : parsed.toISOString();
    }
    const numericCandidate  trimmed.replace(NUMERIC_CLEANER, '');
    if (numericCandidate && /^-?\d+(\.\d+)?$/.test(numericCandidate)) {
      const parsed  Number(numericCandidate);
      return Number.isNaN(parsed) ? null : parsed;
    return trimmed;
  }
export function normaliseRecords(
  workbookName: string,
  rows: NormalizedRecord[]
): NormalizedRecord[] {
  const refreshDate  new Date().toISOString();
  return rows.map((row)  {
    const normalized: NormalizedRecord  {
      workbook_name: workbookName,
      refresh_date: refreshDate,
    };
    Object.entries(row).forEach(([key, value])  {
      if (!key) return;
      const normalKey  snakeCase(key);
      if (!normalKey) return;
      normalized[normalKey]  normaliseValue(normalKey, value);
    });
    return normalized;
  });
export async function getSupabaseClient(config: IngestionConfig): PromiseSupabaseClient {
  return createClient(config.supabaseUrl, config.supabaseKey);
async function initDrive(config: IngestionConfig) {
  const auth  new google.auth.GoogleAuth({
    credentials: {
      client_email: config.serviceAccountEmail,
      private_key: config.privateKey,
    },
    scopes: ['https://www.googleapis.com/auth/drive.readonly'],
  return google.drive({ version: 'v3', auth });
function mapToTable(fileName: string): string | null {
  const lowerName  fileName.toLowerCase();
  for (const { pattern, table } of FILE_PATTERNS) {
    if (pattern.test(lowerName)) return table;
  return null;
export async function ingestFromDrive(): Promisevoid {
  const config  loadIngestionConfig();
  const supabase  await getSupabaseClient(config);
  const drive  await initDrive(config);
  try {
    // List files in shared folder
    const query  `'${config.driveFolderId}' in parents and mimeType ! 'application/vnd.google-apps.folder' and trashed  false`;
    const response  await drive.files.list({
      q: query,
      fields: 'files(id, name, mimeType)',
    const files  response.data.files || [];
    for (const file of files) {
      const fileId  file.id!;
      const fileName  file.name!;
      const mimeType  file.mimeType!;
      // Download file
      const request  await drive.files.get(
        { fileId, alt: 'media' },
        { responseType: 'stream' }
      );
      const chunks: Buffer[]  [];
      const stream  request.data as Readable;
      await new Promisevoid((resolve, reject)  {
        stream.on('data', (chunk)  chunks.push(chunk));
        stream.on('end', resolve);
        stream.on('error', reject);
      });
      const buffer  Buffer.concat(chunks);
      // Read based on type
      let df: any[]  [];
      if (mimeType  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
          fileName.toLowerCase().endsWith('.xlsx')) {
        const workbook  XLSX.read(buffer, { type: 'buffer' });
        const sheetName  workbook.SheetNames[0];
        const worksheet  workbook.Sheets[sheetName];
        df  XLSX.utils.sheet_to_json(worksheet);
      } else if (mimeType  'text/csv' || fileName.toLowerCase().endsWith('.csv')) {
        const csvText  buffer.toString('utf-8');
        const workbook  XLSX.read(csvText, { type: 'string' });
      } else {
        console.warn(`Skipping unsupported file: $fileName`);
        continue;
      }
      const normalizedData  normaliseRecords(fileName, df);
      // Map to staging table
      const table  mapToTable(fileName);
      if (!table) {
        console.warn(`Unknown file pattern: $fileName`);
      // Upsert to Supabase
      const { error }  await supabase
        .from(table)
        .upsert(normalizedData, { onConflict: 'id' });
      if (error) throw error;
      console.log(`Upserted ${normalizedData.length} rows to $table from $fileName`);
    // Refresh ML features
    const { error: refreshError }  await supabase.rpc('refresh_ml_features');
    if (refreshError) throw refreshError;
    console.log('ML features refreshed.');
  } catch (error) {
    console.error('Ingestion failed:', error);
    throw error;

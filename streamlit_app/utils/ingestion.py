"""
Data Ingestion Module - Google Drive to Supabase
Handles 9+ source types with robust normalization and validation

import pandas as pd
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import io
import warnings
warnings.filterwarnings('ignore')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from supabase import create_client

class DataIngestionEngine:
    """Enterprise-grade data ingestion with normalization and validation"""
    
    # Required columns for each source type
    REQUIRED_COLUMNS  {
        'portfolio': ['customer_id', 'balance', 'date'],
        'facility': ['facility_id', 'customer_id', 'limit'],
        'customer': ['customer_id', 'name'],
        'payment': ['payment_id', 'customer_id', 'amount', 'date'],
        'risk': ['customer_id', 'dpd', 'date'],
        'revenue': ['customer_id', 'revenue', 'date'],
        'collections': ['customer_id', 'collected_amount', 'date'],
        'marketing': ['customer_id', 'channel', 'acquisition_date'],
        'industry': ['customer_id', 'industry_code']
    }
    
    def __init__(self, supabase_url: str, supabase_key: str, gdrive_credentials: Dict):
        """Initialize clients"""
        self.supabase  create_client(supabase_url, supabase_key)
        
        credentials  service_account.Credentials.from_service_account_info(
            gdrive_credentials,
            scopes['https://www.googleapis.com/auth/drive.readonly']
        )
        self.drive  build('drive', 'v3', credentialscredentials)
        
    def normalize_columns(self, df: pd.DataFrame) - pd.DataFrame:
        """
        Normalize column names to lowercase with underscores
        Requirement 1: lowercase/underscore column names
        df.columns  [
            re.sub(r'[^a-z0-9_]', '_', col.lower().strip().replace(' ', '_'))
            for col in df.columns
        ]
        # Remove duplicate underscores
        df.columns  [re.sub(r'_+', '_', col).strip('_') for col in df.columns]
        return df
    
    def convert_numeric_tolerant(self, series: pd.Series) - pd.Series:
        Tolerant numeric conversion - removes currency symbols, commas
        Requirement 1: tolerant numeric conversion
        if series.dtype  'object':
            # Remove currency symbols and formatting
            series  series.astype(str).str.replace(r'[\$,₡,€,%]', '', regexTrue)
            series  series.str.replace(',', '', regexTrue)
            series  series.str.strip()
            # Convert to numeric, coerce errors to NaN
            series  pd.to_numeric(series, errors'coerce')
        return series
    
    def standardize_dates(self, df: pd.DataFrame) - pd.DataFrame:
        Standardize date columns to datetime
        Requirement 1: date standardization
        date_columns  [col for col in df.columns if 'date' in col or 'fecha' in col]
        for col in date_columns:
            df[col]  pd.to_datetime(df[col], errors'coerce')
    
    def normalize_dataframe(self, df: pd.DataFrame, source_name: str) - pd.DataFrame:
        Complete normalization pipeline
        Requirement 1: robust handling with deduplication and state saving
        # Step 1: Normalize column names
        df  self.normalize_columns(df)
        
        # Step 2: Convert numeric columns
        for col in df.columns:
            if col not in ['workbook_name', 'refresh_date'] and 'id' not in col and 'name' not in col:
                df[col]  self.convert_numeric_tolerant(df[col])
        
        # Step 3: Standardize dates
        df  self.standardize_dates(df)
        
        # Step 4: Add metadata
        df['workbook_name']  source_name
        df['refresh_date']  datetime.now()
        
        # Step 5: Deduplication
        initial_rows  len(df)
        df  df.drop_duplicates()
        duplicates_removed  initial_rows - len(df)
        
        return df, duplicates_removed
    
    def validate_required_columns(self, df: pd.DataFrame, source_type: str) - Tuple[bool, List[str]]:
        Validate that required columns are present
        Requirement 1: skip if core missing with alert
        if source_type not in self.REQUIRED_COLUMNS:
            return True, []  # Unknown source type, allow
        
        required  self.REQUIRED_COLUMNS[source_type]
        missing  [col for col in required if col not in df.columns]
        
        return len(missing)  0, missing
    
    def calculate_data_quality_score(self, df: pd.DataFrame) - Dict:
        Calculate data quality metrics
        Requirement 8: Data Quality Audit with score %, nulls, zero-rows
        total_cells  df.shape[0] * df.shape[1]
        null_cells  df.isnull().sum().sum()
        null_percentage  (null_cells / total_cells * 100) if total_cells  0 else 0
        
        # Zero rows check (rows with all zeros)
        numeric_cols  df.select_dtypes(include[np.number]).columns
        if len(numeric_cols)  0:
            zero_rows  (df[numeric_cols]  0).all(axis1).sum()
        else:
            zero_rows  0
        
        # Completeness score (100% - null%)
        completeness_score  100 - null_percentage
        
        # Critical column penalty
        critical_cols  ['customer_id', 'balance', 'amount', 'date']
        critical_nulls  0
        for col in critical_cols:
            if col in df.columns:
                critical_nulls + df[col].isnull().sum()
        
        # Penalize critical nulls heavily
        critical_penalty  (critical_nulls / len(df) * 50) if len(df)  0 else 0
        
        final_score  max(0, completeness_score - critical_penalty)
        
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'null_cells': int(null_cells),
            'null_percentage': round(null_percentage, 2),
            'zero_rows': int(zero_rows),
            'completeness_score': round(completeness_score, 2),
            'critical_penalty': round(critical_penalty, 2),
            'final_quality_score': round(final_score, 2)
        }
    
    def detect_source_type(self, filename: str) - Optional[str]:
        """Detect source type from filename"""
        filename_lower  filename.lower()
        
        type_keywords  {
            'portfolio': ['portfolio', 'portafolio', 'cartera', 'balances'],
            'facility': ['facility', 'facilities', 'linea', 'credito', 'limite'],
            'customer': ['customer', 'cliente', 'clients'],
            'payment': ['payment', 'pago', 'pagos', 'cobro'],
            'risk': ['risk', 'riesgo', 'dpd', 'mora'],
            'revenue': ['revenue', 'ingreso', 'ingresos'],
            'collections': ['collection', 'cobranza', 'recuperacion'],
            'marketing': ['marketing', 'adquisicion', 'canal'],
            'industry': ['industry', 'industria', 'sector']
        
        for source_type, keywords in type_keywords.items():
            if any(keyword in filename_lower for keyword in keywords):
                return source_type
        
        return None
    
    def get_table_name(self, source_type: str) - str:
        """Map source type to Supabase table name"""
        table_map  {
            'portfolio': 'raw_portfolios',
            'facility': 'raw_facilities',
            'customer': 'raw_customers',
            'payment': 'raw_payments',
            'risk': 'raw_risk_events',
            'revenue': 'raw_revenue',
            'collections': 'raw_collections',
            'marketing': 'raw_marketing',
            'industry': 'raw_industry'
        return table_map.get(source_type, 'raw_unknown')
    
    def ingest_from_drive(self, folder_id: str) - Dict:
        Main ingestion pipeline: Google Drive → Supabase
        Returns detailed ingestion report
        ingestion_report  {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'details': [],
            'quality_scores': {}
        
        try:
            # List files in Google Drive folder
            query  f"'{folder_id}' in parents and trashed  false"
            results  self.drive.files().list(
                qquery,
                fields"files(id, name, mimeType, modifiedTime, size)"
            ).execute()
            
            files  results.get('files', [])
            ingestion_report['total_files']  len(files)
            
            for file_info in files:
                file_id  file_info['id']
                file_name  file_info['name']
                mime_type  file_info['mimeType']
                
                file_result  {
                    'filename': file_name,
                    'status': 'unknown',
                    'message': '',
                    'rows_processed': 0,
                    'duplicates_removed': 0
                }
                
                try:
                    # Download file
                    request  self.drive.files().get_media(fileIdfile_id)
                    fh  io.BytesIO()
                    downloader  MediaIoBaseDownload(fh, request)
                    done  False
                    while not done:
                        status, done  downloader.next_chunk()
                    fh.seek(0)
                    
                    # Parse file based on type
                    if mime_type.endswith('spreadsheetml.sheet') or file_name.endswith('.xlsx'):
                        df  pd.read_excel(fh)
                    elif mime_type  'text/csv' or file_name.endswith('.csv'):
                        df  pd.read_csv(fh)
                    else:
                        file_result['status']  'skipped'
                        file_result['message']  f'Unsupported file type: {mime_type}'
                        ingestion_report['skipped'] + 1
                        ingestion_report['details'].append(file_result)
                        continue
                    
                    # Detect source type
                    source_type  self.detect_source_type(file_name)
                    if not source_type:
                        file_result['message']  'Could not detect source type from filename'
                    
                    # Normalize data
                    df, duplicates_removed  self.normalize_dataframe(df, file_name)
                    
                    # Validate required columns
                    is_valid, missing_cols  self.validate_required_columns(df, source_type)
                    if not is_valid:
                        file_result['status']  'failed'
                        file_result['message']  f'Missing required columns: {", ".join(missing_cols)}'
                        ingestion_report['failed'] + 1
                    
                    # Calculate quality score
                    quality_metrics  self.calculate_data_quality_score(df)
                    ingestion_report['quality_scores'][file_name]  quality_metrics
                    
                    # Get target table
                    table_name  self.get_table_name(source_type)
                    
                    # Convert to records
                    data  df.to_dict(orient'records')
                    
                    # Upsert to Supabase
                    # Note: Requires unique constraint on customer_id + date or similar
                    response  self.supabase.table(table_name).upsert(
                        data,
                        on_conflict'id' if 'id' in df.columns else None
                    ).execute()
                    
                    file_result['status']  'success'
                    file_result['message']  f'Upserted {len(data)} rows to {table_name}'
                    file_result['rows_processed']  len(data)
                    file_result['duplicates_removed']  duplicates_removed
                    file_result['quality_score']  quality_metrics['final_quality_score']
                    ingestion_report['successful'] + 1
                    
                except Exception as e:
                    file_result['status']  'failed'
                    file_result['message']  f'Error: {str(e)}'
                    ingestion_report['failed'] + 1
                
                ingestion_report['details'].append(file_result)
            
            # Refresh ML features if any data was ingested
            if ingestion_report['successful']  0:
                    self.supabase.rpc('refresh_ml_features').execute()
                    ingestion_report['ml_features_refreshed']  True
                    ingestion_report['ml_features_refreshed']  False
                    ingestion_report['ml_refresh_error']  str(e)
            
        except Exception as e:
            ingestion_report['error']  str(e)
        
        return ingestion_report

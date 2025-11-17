/* eslint-disable */
// Auto-generated database types
export interface Database {
  public: {
    Tables: {
      customers: {
        Row: {
          id: string;
          customer_id: string;
          client_type: string;
          internal_credit_score: number | null;
          external_credit_score: number | null;
          equifax_score: number | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          internal_credit_score?: number | null;
          external_credit_score?: number | null;
          equifax_score?: number | null;
          created_at?: string;
          updated_at?: string;
        Update: {
          customer_id?: string;
          client_type?: string;
      };
    };
    Views: Recordstring, never;
    Functions: Recordstring, never;
    Enums: Recordstring, never;
  };
}

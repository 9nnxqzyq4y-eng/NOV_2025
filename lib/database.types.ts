export type Database  {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          created_at: string;
          email: string;
          full_name: string | null;
          avatar_url: string | null;
        }
        Insert: {
          created_at?: string;
          full_name?: string | null;
          avatar_url?: string | null;
        Update: {
          id?: string;
          email?: string;
      }
    }
    Views: Record;
    Functions: Record;
    Enums: Record;
  }
}

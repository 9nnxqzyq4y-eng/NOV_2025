interface HubSpotResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

interface HubSpotContact {
  id: string;
  properties: {
    email?: string;
    firstname?: string;
    lastname?: string;
    company?: string;
  };

interface HubSpotDeal {
    dealname?: string;
    amount?: string;
    dealstage?: string;
    closedate?: string;

class HubSpotIntegration {
  private apiKey: string;
  private baseUrl = 'https://api.hubapi.com';

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<HubSpotResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}$endpoint`, {
        ...options,
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      const data = await response.json().catch(() => undefined);
      
      return {
        data,
        status: response.status,
        error: response.ok ? undefined : data?.message || 'Request failed',
      };
    } catch (error) {
        status: 500,
        error: error instanceof Error ? error.message : 'Unknown error',
    }

  async getContacts(): Promise<HubSpotResponse<HubSpotContact[]>> {
    return this.makeRequest<HubSpotContact[]>('/crm/v3/objects/contacts');

  async getDeals(): Promise<HubSpotResponse<HubSpotDeal[]>> {
    return this.makeRequest<HubSpotDeal[]>('/crm/v3/objects/deals');

export { HubSpotIntegration, type HubSpotContact, type HubSpotDeal, type HubSpotResponse };

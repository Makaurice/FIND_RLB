import axios from 'axios';

export const aiAgentsAPI = {
  tenant: async (user_id: string, preferences: any, properties: any[]) =>
    axios.post('/api/ai/tenant', { user_id, preferences, properties }),
  landlord: async (landlord_id: string, property: any, market_data: any, history: any[], lease: any, tenant: string) =>
    axios.post('/api/ai/landlord', { landlord_id, property, market_data, history, lease, tenant }),
  match: async (tenants: any[], properties: any[]) =>
    axios.post('/api/ai/match', { tenants, properties }),
};

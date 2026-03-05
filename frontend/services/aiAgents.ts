import axios from 'axios';

export const aiAgentsAPI = {
  tenant: async (user_id: string, preferences: any, properties: any[]) =>
    axios.post('/api/ai/tenant', { user_id, preferences, properties }),
  landlord: async (landlord_id: string, property: any, market_data: any, history: any[], lease: any, tenant: string) =>
    axios.post('/api/ai/landlord', { landlord_id, property, market_data, history, lease, tenant }),
  match: async (tenants: any[], properties: any[]) =>
    axios.post('/api/ai/match', { tenants, properties }),
  customerCare: async (user_id: string, message: string, session_id?: string, context?: any) =>
    axios.post('/api/ai/customer-care', { user_id, message, session_id, context }),
};

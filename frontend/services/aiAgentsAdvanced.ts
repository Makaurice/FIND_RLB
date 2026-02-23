import axios from 'axios';

export const aiAgentsAdvancedAPI = {
  topMatches: async (tenants: any[], properties: any[], n: number = 3) =>
    axios.post('/api/ai/top-matches', { tenants, properties, n }),
  advancedTenantRecommendation: async (user_id: string, preferences: any) =>
    axios.post('/api/ai/tenant/advanced', { user_id, preferences }),
};

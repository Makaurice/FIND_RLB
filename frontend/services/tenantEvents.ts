import axios from 'axios';

export const tenantEventsAPI = {
  getEvents: async () => axios.get('/api/contracts/tenant/events'),
};

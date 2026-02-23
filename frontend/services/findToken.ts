import axios from 'axios';

export const findTokenAPI = {
  getBalance: async (address: string) => axios.get(`/api/token/balance/${address}`),
  transfer: async (from: string, to: string, amount: number) => axios.post('/api/token/transfer', { from, to, amount }),
  claimTeam: async () => axios.post('/api/token/claim-team'),
};

import axios from 'axios';

export const rentalHistoryAPI = {
  getHistory: async () => axios.get('/api/contracts/rental/history'),
};

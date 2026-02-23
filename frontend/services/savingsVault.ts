import axios from 'axios';

export const savingsVaultAPI = {
  deposit: async (planId: number, amount: number) => axios.post(`/api/savings/${planId}/deposit`, { amount }),
  autoMatch: async (planId: number, propertyId: number) => axios.post(`/api/savings/${planId}/match`, { propertyId }),
  convertToOwnership: async (planId: number) => axios.post(`/api/savings/${planId}/convert`, {}),
};

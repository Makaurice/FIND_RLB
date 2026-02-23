import axios from 'axios';

export const rentEscrowAPI = {
  payRent: async (leaseId: number, amount: number) => axios.post(`/api/rent/${leaseId}/pay`, { amount }),
  chargeLatePenalty: async (leaseId: number) => axios.post(`/api/rent/${leaseId}/late`, {}),
};

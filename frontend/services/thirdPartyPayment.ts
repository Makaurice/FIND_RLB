import axios from 'axios';

export const thirdPartyPaymentAPI = {
  payOnBehalf: async (tenant: string, leaseId: number, amount: number) => axios.post(`/api/thirdparty/pay`, { tenant, leaseId, amount }),
};

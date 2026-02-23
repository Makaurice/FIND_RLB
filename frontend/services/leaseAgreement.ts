import axios from 'axios';

export const leaseAgreementAPI = {
  create: async (data: any) => axios.post('/api/lease/create', data),
  activate: async (leaseId: number) => axios.post(`/api/lease/${leaseId}/activate`, {}),
  terminate: async (leaseId: number) => axios.post(`/api/lease/${leaseId}/terminate`, {}),
  renew: async (leaseId: number, newEndDate: number) => axios.post(`/api/lease/${leaseId}/renew`, { newEndDate }),
};

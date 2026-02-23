import axios from 'axios';

export const reputationAPI = {
  updatePaymentConsistency: async (user: string, score: number) => axios.post(`/api/reputation/${user}/payment`, { score }),
  updateLeaseCompletionRate: async (user: string, score: number) => axios.post(`/api/reputation/${user}/lease`, { score }),
  updateReviewsScore: async (user: string, score: number) => axios.post(`/api/reputation/${user}/reviews`, { score }),
};

import axios from 'axios';

export const propertyNFTAPI = {
  register: async (data: {
    location: string;
    metadataURI: string;
    forRent: boolean;
    forSale: boolean;
    price: number;
  }) => {
    return axios.post('/api/property/register', data);
  },
  // Add more contract actions as needed
};

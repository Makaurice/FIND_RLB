import { API_ENDPOINTS } from '../config/api';

interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  errors?: any;
}

interface AuthTokens {
  access: string;
  refresh: string;
}

interface AuthUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'tenant' | 'landlord' | 'service_provider' | 'admin';
  is_verified: boolean;
  created_at: string;
}

interface AuthResponse {
  access: string;
  refresh: string;
  user: AuthUser;
}

// Token management
const getTokens = (): AuthTokens | null => {
  if (typeof window === 'undefined') return null;
  const access = localStorage.getItem('access_token');
  const refresh = localStorage.getItem('refresh_token');
  return access && refresh ? { access, refresh } : null;
};

const setTokens = (tokens: AuthTokens) => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
};

const clearTokens = () => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};

// Generic API fetch function
async function apiCall<T = any>(
  url: string,
  options: RequestInit = {},
  includeAuth: boolean = true
): Promise<ApiResponse<T>> {
  try {
    const headers: any = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add auth token if available
    if (includeAuth) {
      const tokens = getTokens();
      if (tokens?.access) {
        headers['Authorization'] = `Bearer ${tokens.access}`;
      }
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: data?.detail || data?.error || 'An error occurred',
        errors: data,
      };
    }

    return {
      success: true,
      data,
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Network error',
    };
  }
}

// Authentication API calls
export const authAPI = {
  register: async (userData: {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password: string;
    password2: string;
    role: string;
  }): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiCall<AuthResponse>(
      API_ENDPOINTS.REGISTER,
      {
        method: 'POST',
        body: JSON.stringify(userData),
      },
      false
    );

    if (response.success && response.data) {
      setTokens({
        access: response.data.access,
        refresh: response.data.refresh,
      });
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response;
  },

  login: async (credentials: {
    username: string;
    password: string;
  }): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiCall<AuthResponse>(
      API_ENDPOINTS.LOGIN,
      {
        method: 'POST',
        body: JSON.stringify(credentials),
      },
      false
    );

    if (response.success && response.data) {
      setTokens({
        access: response.data.access,
        refresh: response.data.refresh,
      });
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response;
  },

  logout: async (): Promise<ApiResponse> => {
    const tokens = getTokens();
    if (!tokens?.refresh) {
      clearTokens();
      return { success: true };
    }

    const response = await apiCall(
      API_ENDPOINTS.LOGOUT,
      {
        method: 'POST',
        body: JSON.stringify({ refresh: tokens.refresh }),
      },
      true
    );

    clearTokens();
    return response;
  },

  verify: async (): Promise<ApiResponse<AuthResponse>> => {
    return apiCall<AuthResponse>(
      API_ENDPOINTS.VERIFY,
      { method: 'GET' },
      true
    );
  },

  refreshToken: async (): Promise<ApiResponse<{ access: string }>> => {
    const tokens = getTokens();
    if (!tokens?.refresh) {
      return { success: false, error: 'No refresh token available' };
    }

    const response = await apiCall<{ access: string }>(
      API_ENDPOINTS.REFRESH,
      {
        method: 'POST',
        body: JSON.stringify({ refresh: tokens.refresh }),
      },
      false
    );

    if (response.success && response.data?.access) {
      setTokens({
        access: response.data.access,
        refresh: tokens.refresh,
      });
    }

    return response;
  },

  getProfile: async (): Promise<ApiResponse<AuthUser>> => {
    return apiCall<AuthUser>(
      API_ENDPOINTS.PROFILE,
      { method: 'GET' },
      true
    );
  },

  updateProfile: async (profileData: Partial<AuthUser>): Promise<ApiResponse<AuthUser>> => {
    return apiCall<AuthUser>(
      API_ENDPOINTS.PROFILE,
      {
        method: 'PUT',
        body: JSON.stringify(profileData),
      },
      true
    );
  },

  getCurrentUser: (): AuthUser | null => {
    if (typeof window === 'undefined') return null;
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  isAuthenticated: (): boolean => {
    const tokens = getTokens();
    return !!tokens?.access;
  },
};

// Properties API calls
export const propertiesAPI = {
  getAll: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.PROPERTIES, { method: 'GET' }, true);
  },

  create: async (propertyData: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.PROPERTIES,
      {
        method: 'POST',
        body: JSON.stringify(propertyData),
      },
      true
    );
  },
};

// Tenant API calls
export const tenantAPI = {
  getAll: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.TENANTS, { method: 'GET' }, true);
  },

  create: async (tenantData: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.TENANTS,
      {
        method: 'POST',
        body: JSON.stringify(tenantData),
      },
      true
    );
  },
};

// Landlord API calls
export const landlordAPI = {
  getListings: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.LANDLORD_LISTINGS, { method: 'GET' }, true);
  },

  createListing: async (data: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.LANDLORD_LISTINGS,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      true
    );
  },

  getPricing: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.LANDLORD_PRICING, { method: 'GET' }, true);
  },

  updatePricing: async (data: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.LANDLORD_PRICING,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      true
    );
  },

  getSchedules: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.LANDLORD_SCHEDULES, { method: 'GET' }, true);
  },

  createSchedule: async (data: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.LANDLORD_SCHEDULES,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      true
    );
  },

  getHistory: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.LANDLORD_HISTORY, { method: 'GET' }, true);
  },

  getAnalytics: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.LANDLORD_ANALYTICS, { method: 'GET' }, true);
  },
};

// Service Provider API calls
export const serviceAPI = {
  getMovers: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.SERVICE_MOVERS, { method: 'GET' }, true);
  },

  getBookings: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.SERVICE_BOOKINGS, { method: 'GET' }, true);
  },

  createBooking: async (data: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.SERVICE_BOOKINGS,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      true
    );
  },

  getMaintenance: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.SERVICE_MAINTENANCE, { method: 'GET' }, true);
  },

  createMaintenance: async (data: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.SERVICE_MAINTENANCE,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      true
    );
  },

  getStorage: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.SERVICE_STORAGE, { method: 'GET' }, true);
  },

  getInventory: async (): Promise<ApiResponse> => {
    return apiCall(API_ENDPOINTS.SERVICE_INVENTORY, { method: 'GET' }, true);
  },

  createInventory: async (data: any): Promise<ApiResponse> => {
    return apiCall(
      API_ENDPOINTS.SERVICE_INVENTORY,
      {
        method: 'POST',
        body: JSON.stringify(data),
      },
      true
    );
  },
};

// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export const API_ENDPOINTS = {
  // Auth endpoints
  REGISTER: `${API_BASE_URL}/api/auth/register/`,
  LOGIN: `${API_BASE_URL}/api/auth/login/`,
  LOGOUT: `${API_BASE_URL}/api/auth/logout/`,
  VERIFY: `${API_BASE_URL}/api/auth/verify/`,
  REFRESH: `${API_BASE_URL}/api/auth/refresh/`,
  PROFILE: `${API_BASE_URL}/api/auth/profile/`,

  // Property endpoints
  PROPERTIES: `${API_BASE_URL}/api/properties/`,

  // Tenant endpoints
  TENANTS: `${API_BASE_URL}/api/tenants/`,

  // Landlord endpoints
  LANDLORD_LISTINGS: `${API_BASE_URL}/api/landlord/listings/`,
  LANDLORD_PRICING: `${API_BASE_URL}/api/landlord/pricing/`,
  LANDLORD_SCHEDULES: `${API_BASE_URL}/api/landlord/schedules/`,
  LANDLORD_HISTORY: `${API_BASE_URL}/api/landlord/history/`,
  LANDLORD_ANALYTICS: `${API_BASE_URL}/api/landlord/analytics/`,

  // Service endpoints
  SERVICE_MOVERS: `${API_BASE_URL}/api/service/movers/`,
  SERVICE_BOOKINGS: `${API_BASE_URL}/api/service/bookings/`,
  SERVICE_MAINTENANCE: `${API_BASE_URL}/api/service/maintenance/`,
  SERVICE_STORAGE: `${API_BASE_URL}/api/service/storage/`,
  SERVICE_INVENTORY: `${API_BASE_URL}/api/service/inventory/`,
};

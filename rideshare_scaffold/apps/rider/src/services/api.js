import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    try {
      const token = await SecureStore.getItemAsync('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error getting auth token:', error);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear it
      await SecureStore.deleteItemAsync('authToken');
      // You might want to redirect to login here
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  requestMagicLink: (email, phone, role) => 
    api.post('/auth/magic-link', { email, phone, role }),
  
  verifyCode: (email, phone, code) => 
    api.post('/auth/verify', { email, phone, code }),
  
  getProfile: () => api.get('/auth/me'),
};

// Rides API
export const ridesAPI = {
  getQuote: (rideRequest) => 
    api.post('/rides/quote', rideRequest),
  
  requestRide: (rideRequest) => 
    api.post('/rides/request', rideRequest),
  
  getRides: () => api.get('/rides'),
  
  getRide: (rideId) => api.get(`/rides/${rideId}`),
  
  cancelRide: (rideId) => api.post(`/rides/${rideId}/cancel`),
  
  updateRideStatus: (rideId, status) => 
    api.put(`/rides/${rideId}/status`, { status }),
};

// Tips API
export const tipsAPI = {
  createTip: (tipRequest) => 
    api.post('/tips', tipRequest),
  
  getTips: () => api.get('/tips'),
  
  getTip: (tipId) => api.get(`/tips/${tipId}`),
};

// Payment API
export const paymentAPI = {
  createPaymentIntent: (amount, currency = 'usd') => 
    api.post('/payments/create-intent', { amount, currency }),
  
  confirmPayment: (paymentIntentId, paymentMethodId) => 
    api.post('/payments/confirm', { paymentIntentId, paymentMethodId }),
};

export { api };

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const pregnancyAPI = {
  // Ask a pregnancy health question
  askQuestion: async (question) => {
    try {
      const response = await api.post('/api/v1/ai/ask', {
        question: question
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get answer');
    }
  },

  // Get API health status
  getHealth: async () => {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw new Error('API is not available');
    }
  },

  // Get API documentation URL
  getDocsUrl: () => {
    return `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/docs`;
  }
};

export default api; 
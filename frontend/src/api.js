import axios from "axios";

// Set your default API base URL
const defaultApiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

// Create an axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || defaultApiUrl,
  withCredentials: true, // ⬅️ Enables sending cookies (sessionid, csrftoken)
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Optional: Add a response interceptor to handle auth-related errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Automatically redirect to login on 401/403
      if (error.response.status === 401 || error.response.status === 403) {
        console.warn("Authentication error. Redirecting to login...");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;

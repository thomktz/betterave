import axios from 'axios';
import { th } from 'date-fns/locale';
import { useToast } from 'vue-toastification';

// Create an Axios instance
const apiClient = axios.create({
  withCredentials: true,
  baseURL: process.env.VUE_APP_API_URL,
});

console.log("Using API URL:", process.env.VUE_APP_API_URL);

// Create toast instance
const toast = useToast();

// Add a request interceptor
apiClient.interceptors.request.use(
  request => {
    // Log the full request details here
    // console.log("Starting Request", JSON.stringify(request, null, 2));
    return request;
  },
  error => {
    // Do something with request error
    c// onsole.error("Request Error:", error);
    return Promise.reject(error);
  }
);


// Add a response interceptor
apiClient.interceptors.response.use(
  response => {
    // Your response success handling
    return response;
  },
  error => {
    // Check if the error is an expected one
    if (error.response && error.response.status === 401 && error.config.url.includes('/check-auth')) {
      // This is an expected error, so we don't show an error message
      console.log('User not authenticated, expected behavior');
    } else {
      // For other errors, display the error message
      const message = (error.response && error.response.data && error.response.data.message) || 
                      error.message || 
                      'An unknown error occurred';
      toast.error(message);
      return Promise.reject(error);
    }
  }
);

export { apiClient, toast };

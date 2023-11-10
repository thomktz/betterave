import axios from 'axios';
import { useToast } from 'vue-toastification';

// Create an Axios instance
const apiClient = axios.create({
  withCredentials: true,
  baseURL: process.env.VUE_APP_API_URL,
});

console.log("Using API URL:", process.env.VUE_APP_API_URL);

// Create toast instance
const toast = useToast();

// Add a response interceptor
apiClient.interceptors.response.use(
  response => {
    // Your response success handling
    console.log("Response:", response);
    return response;
  },
  error => {
    // Your error handling
    const message =
      (error.response && error.response.data && error.response.data.message) ||
      error.message ||
      'An unknown error occurred';

    // Display the error message
    toast.error(message);

    // Handle error logging or display here if needed
    console.error("Caught error:", error);
  }
);

export default apiClient;

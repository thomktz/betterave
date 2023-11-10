import axios from 'axios';

// Allow cookies to be sent with requests
axios.defaults.withCredentials = true;

// Get the base URL from the .env file
axios.defaults.baseURL = process.env.VUE_APP_API_URL;
console.log("Using API URL:", process.env.VUE_APP_API_URL);
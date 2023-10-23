import axios from 'axios';
import { API_BASE_URL } from './apiConfig';

axios.defaults.baseURL = API_BASE_URL;
console.log(`axios.defaults.baseURL: ${axios.defaults.baseURL}`);
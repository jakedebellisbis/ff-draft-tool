import axios from 'axios';

// Use the Vercel/Local env var. No trailing slash.
const baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8011';

export const api = axios.create({ baseURL });




import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

const SESSION_ID = crypto.randomUUID();

export const sendMessage = (message) =>
  API.post('/chat', { message, session_id: SESSION_ID });

export const getListings = (filters = {}) =>
  API.get('/listings', { params: filters });
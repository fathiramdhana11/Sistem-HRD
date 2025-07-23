// File: frontend/src/services/utils.js

export const API_URL = 'http://127.0.0.1:8000';

export const getAuthHeaders = () => {
  const auth = JSON.parse(localStorage.getItem('auth'));
  const token = auth?.access_token;

  if (!token) {
    console.error("Token otentikasi tidak ditemukan di localStorage.");
    return {};
  }

  return { Authorization: `Bearer ${token}` };
};
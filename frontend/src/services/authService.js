// File: frontend/src/services/authService.js

import axios from 'axios';

// Definisikan base URL API Anda. Sebaiknya ini ditaruh di file .env nanti.
const API_URL = 'http://127.0.0.1:8000';

const login = (username, password) => {
  // Backend FastAPI kita (dengan OAuth2PasswordRequestForm) mengharapkan
  // data dikirim dalam format 'form-data', bukan JSON.
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  // Panggil endpoint yang benar (/api/token) dengan data dan header yang tepat
  return axios.post(`${API_URL}/api/token`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
};

const logout = () => {
  // Hapus data dari localStorage
  localStorage.removeItem('auth');
};

export default {
  login,
  logout,
};
// File: frontend/src/services/userService.js

import axios from 'axios';
import { getAuthHeaders, API_URL } from './utils';

const getUsers = () => {
  return axios.get(`${API_URL}/api/users`, { headers: getAuthHeaders() });
};

// --- FUNGSI BARU UNTUK MEMBUAT PENGGUNA ---
const createUser = (userData) => {
  return axios.post(`${API_URL}/api/users`, userData, { 
    headers: getAuthHeaders() 
  });
};

// --- FUNGSI BARU UNTUK MENGUPDATE PENGGUNA ---
const updateUser = (userId, userData) => {
  return axios.put(`${API_URL}/api/users/${userId}`, userData, {
    headers: getAuthHeaders()
  });
};

// --- FUNGSI BARU UNTUK MENGHAPUS PENGGUNA ---
const deleteUser = (userId) => {
  return axios.delete(`${API_URL}/api/users/${userId}`, {
    headers: getAuthHeaders()
  });
};


export default {
  getUsers,
  createUser,
  updateUser,
  deleteUser,
};
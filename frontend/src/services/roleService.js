// File: frontend/src/services/roleService.js

import axios from 'axios';
import { getAuthHeaders, API_URL } from './utils';

const getRoles = () => {
  return axios.get(`${API_URL}/api/roles`, {
    headers: getAuthHeaders()
  });
};

const createRole = (roleData) => {
  return axios.post(`${API_URL}/api/roles`, roleData, {
    headers: getAuthHeaders()
  });
};

const updateRole = (roleId, roleData) => {
  return axios.put(`${API_URL}/api/roles/${roleId}`, roleData, {
    headers: getAuthHeaders()
  });
};

const deleteRole = (roleId) => {
  return axios.delete(`${API_URL}/api/roles/${roleId}`, {
    headers: getAuthHeaders()
  });
};

export default { getRoles, createRole, updateRole, deleteRole };
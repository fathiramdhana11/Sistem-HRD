// File: frontend/src/services/roleService.js

import axios from 'axios';
import { getAuthHeaders, API_URL } from './utils';

const getRoles = () => {
  return axios.get(`${API_URL}/api/roles`, {
    headers: getAuthHeaders()
  });
};

export default { getRoles };
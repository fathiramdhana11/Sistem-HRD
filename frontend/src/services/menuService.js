import axios from "axios";
import { getAuthHeaders, API_URL } from "./utils";

const getMenuTree = () => {
  return axios.get(`${API_URL}/api/menus/tree`, {
    headers: getAuthHeaders(),
  });
};

const getUserMenus = () => {
  const timestamp = Date.now()
  return axios.get(`${API_URL}/api/menus/user-menus?_t=${timestamp}`, {
    headers: {
      ...getAuthHeaders(),
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    }
  }).then(response => {
    console.log('📋 MenuService API response:', response.data)
    return response
  }).catch(error => {
    console.error('❌ MenuService API error:', error)
    // Return empty array on error
    return { data: [] }
  })
}

export default {
  getMenuTree,
  getUserMenus,
};

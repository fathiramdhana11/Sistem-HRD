import axios from "axios";
import { getAuthHeaders, API_URL } from "./utils";

const getAllRoleMenuAccess = () => {
  return axios.get(`${API_URL}/api/role-menu-access`, {
    headers: getAuthHeaders(),
  });
};

const createRoleMenuAccess = (roleMenuAccess) => {
  return axios.post(`${API_URL}/api/role-menu-access`, roleMenuAccess, {
    headers: getAuthHeaders(),
  });
};

const deleteRoleMenuAccess = (roleId, menuId) => {
  return axios.delete(`${API_URL}/api/role-menu-access/${roleId}/${menuId}`, {
    headers: getAuthHeaders(),
  });
};

export default {
  getAllRoleMenuAccess,
  createRoleMenuAccess,
  deleteRoleMenuAccess,
};

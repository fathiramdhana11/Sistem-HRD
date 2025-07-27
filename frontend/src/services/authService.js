import axios from 'axios';
import { API_URL } from './utils';
import { useToast } from '@/composables/useToast';
import router from '@/router';

class AuthService {
  login(user) {
    // Bersihkan localStorage sebelum login untuk mencegah konflik token
    localStorage.removeItem('auth');
    delete axios.defaults.headers.common['Authorization'];
    
    const params = new URLSearchParams();
    params.append('username', user.username);
    params.append('password', user.password);

    return axios.post(`${API_URL}/api/token`, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  }

  refreshToken(refreshToken) {
    return axios.post(`${API_URL}/api/refresh`, {
      refresh_token: refreshToken
    });
  }
}

// Flag untuk mencegah multiple refresh attempts
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

// Enhanced axios interceptor dengan automatic token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const toast = useToast();
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Cek apakah ini bukan request login atau refresh
      if (originalRequest.url.includes('/api/token') || originalRequest.url.includes('/api/refresh')) {
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // Jika sedang refresh, queue request ini
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return axios(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Ambil refresh token dari localStorage
        const authData = JSON.parse(localStorage.getItem('auth'));
        const refreshToken = authData?.refresh_token;

        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        // Coba refresh token
        const response = await axios.post(`${API_URL}/api/refresh`, {
          refresh_token: refreshToken
        });

        const newAccessToken = response.data.access_token;
        
        // Update localStorage dengan token baru
        authData.access_token = newAccessToken;
        localStorage.setItem('auth', JSON.stringify(authData));
        
        // Update default authorization header
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + newAccessToken;
        
        // Process queued requests
        processQueue(null, newAccessToken);
        
        // Retry original request dengan token baru
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;
        return axios(originalRequest);
        
      } catch (refreshError) {
        // Refresh token gagal, lakukan logout
        processQueue(refreshError, null);
        
        localStorage.removeItem('auth');
        delete axios.defaults.headers.common['Authorization'];
        
        toast.error('Sesi Berakhir', 'Sesi Anda telah berakhir. Silakan login kembali.');
        
        setTimeout(() => {
          router.push('/login');
        }, 2000);
        
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    } else if (error.response?.status === 403) {
      // Hanya tampilkan toast jika bukan dari halaman login
      if (!originalRequest.url.includes('/api/token')) {
        toast.error('Akses Ditolak', 'Anda tidak memiliki izin untuk mengakses resource ini.');
      }
    } else if (error.response?.status >= 500) {
      // Hanya tampilkan toast jika bukan dari halaman login
      if (!originalRequest.url.includes('/api/token')) {
        toast.error('Server Error', 'Terjadi kesalahan pada server. Silakan coba lagi nanti.');
      }
    } else if (!error.response) {
      // Hanya tampilkan toast jika bukan dari halaman login
      if (!originalRequest.url.includes('/api/token')) {
        toast.error('Koneksi Error', 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.');
      }
    }
    
    return Promise.reject(error);
  }
);

// Set authorization header dari localStorage saat aplikasi dimuat
const authData = JSON.parse(localStorage.getItem('auth'));
if (authData?.access_token) {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + authData.access_token;
}

export default new AuthService();

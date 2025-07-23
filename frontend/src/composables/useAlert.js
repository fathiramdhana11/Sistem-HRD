// File: frontend/src/composables/useAlert.js

import { useToast } from 'vue-toastification';

export function useAlert() {
  const toast = useToast();

  const success = (message) => {
    toast.success(message || 'Operasi berhasil!');
  };

  const error = (message) => {
    toast.error(message || 'Terjadi kesalahan.');
  };

  const info = (message) => {
    toast.info(message);
  };

  const warning = (message) => {
    toast.warning(message);
  };

  return { success, error, info, warning };
}
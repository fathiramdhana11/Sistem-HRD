import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/auth/'

export function login(payload) {
  return axios.post(API_URL + 'login', payload)
}

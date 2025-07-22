<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded shadow-md w-96">
      <h1 class="text-2xl font-semibold mb-4 text-center">Login HRIS</h1>
      <input v-model="username" placeholder="Username" class="w-full border p-2 mb-3 rounded" />
      <input v-model="password" type="password" placeholder="Password" class="w-full border p-2 mb-3 rounded" />
      <button @click="handleLogin" class="w-full bg-blue-600 text-white p-2 rounded">Login</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const res = await axios.post('http://localhost:8000/auth/login', {
      username: username.value,
      password: password.value
    })

    const { token, user } = res.data
    localStorage.setItem('auth', JSON.stringify({ token, user }))
    router.push('/dashboard')
  } catch (err) {
    alert('Login gagal, periksa username/password')
    console.error(err)
  }
}
</script>

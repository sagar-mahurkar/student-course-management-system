import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { AuthUser } from '../services/auth'
import { login as loginRequest } from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<AuthUser | null>(null)

  const isAuthenticated = computed(() => Boolean(token.value))

  async function login(email: string, password: string) {
    const response = await loginRequest({ email, password })

    token.value = response.data.access_token
    user.value = response.data.user
    localStorage.setItem('access_token', response.data.access_token)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
  }
})

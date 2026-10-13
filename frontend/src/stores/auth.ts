import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { AuthUser } from '../services/auth'
import {
  getCurrentUser,
  login as loginRequest,
} from '../services/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(
    localStorage.getItem('access_token'),
  )

  const user = ref<AuthUser | null>(null)
  const initialized = ref(false)
  let initializationPromise: Promise<void> | null = null

  const isAuthenticated = computed(
    () => Boolean(token.value && user.value),
  )

  async function login(email: string, password: string) {
    const response = await loginRequest({ email, password })

    token.value = response.data.access_token
    user.value = response.data.user

    localStorage.setItem('access_token', response.data.access_token)
    initialized.value = true
  }

  async function fetchCurrentUser(): Promise<void> {
    try {
      user.value = await getCurrentUser()
    } catch (error) {
      token.value = null
      user.value = null

      localStorage.removeItem('access_token')

      throw error
    }
  }

  async function initializeAuth(): Promise<void> {
    if (initialized.value) {
      return
    }

    if (!token.value) {
      user.value = null
      initialized.value = true
      return
    }

    if (!initializationPromise) {
      initializationPromise = (async () => {
        try {
          await fetchCurrentUser()
        } catch {
          // Invalid or expired tokens leave the user logged out.
        } finally {
          initialized.value = true
          initializationPromise = null
        }
      })()
    }

    await initializationPromise
  }

  function logout(): void {
    token.value = null
    user.value = null
    initialized.value = true

    localStorage.removeItem('access_token')
  }

  return {
    token,
    user,
    initialized,
    isAuthenticated,
    login,
    logout,
    fetchCurrentUser,
    initializeAuth,
  }
})

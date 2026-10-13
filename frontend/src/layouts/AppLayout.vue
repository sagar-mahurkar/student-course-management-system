<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const navigationExpanded = ref(false)

function closeNavigation() {
  navigationExpanded.value = false
}

async function handleLogout() {
  authStore.logout()
  closeNavigation()
  await router.push({ name: 'login' })
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm">
    <div class="container">
      <RouterLink
        to="/dashboard"
        class="navbar-brand fw-semibold"
        @click="closeNavigation"
      >
        Student Course Management
      </RouterLink>

      <button
        class="navbar-toggler"
        type="button"
        :aria-expanded="navigationExpanded"
        aria-controls="app-navbar"
        aria-label="Toggle navigation"
        @click="navigationExpanded = !navigationExpanded"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div
        id="app-navbar"
        class="collapse navbar-collapse"
        :class="{ show: navigationExpanded }"
      >
        <div class="navbar-nav me-auto">
          <RouterLink
            to="/dashboard"
            class="nav-link"
            @click="closeNavigation"
          >
            Dashboard
          </RouterLink>
          <RouterLink
            to="/courses"
            class="nav-link"
            @click="closeNavigation"
          >
            {{ authStore.user?.role === 'admin' ? 'Manage Courses' : 'Courses' }}
          </RouterLink>
          <RouterLink
            v-if="authStore.user?.role === 'student'"
            to="/enrollments"
            class="nav-link"
            @click="closeNavigation"
          >
            My Enrollments
          </RouterLink>
        </div>

        <div class="d-flex flex-column flex-lg-row align-items-lg-center gap-2 gap-lg-3 py-2 py-lg-0">
          <div v-if="authStore.user" class="text-lg-end">
            <div class="fw-semibold">{{ authStore.user.full_name }}</div>
            <span class="badge rounded-pill text-bg-secondary small">
              {{ authStore.user.role }}
            </span>
          </div>

          <button
            type="button"
            class="btn btn-outline-secondary btn-sm"
            @click="handleLogout"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>

  <RouterView />
</template>

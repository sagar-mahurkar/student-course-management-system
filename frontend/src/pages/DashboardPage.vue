
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const courseCount = ref<number | null>(null)
const enrollmentCount = ref<number | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const coursesResponse = await api.get('/courses')
    const courses = coursesResponse.data.data
    courseCount.value = Array.isArray(courses) ? courses.length : 0

    if (authStore.user?.role === 'student') {
      const enrollmentsResponse = await api.get('/enrollments')
      const enrollments = enrollmentsResponse.data.data
      enrollmentCount.value = Array.isArray(enrollments)
        ? enrollments.length
        : 0
    }
  } catch {
    error.value = 'Unable to load dashboard information.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="container py-4">
    <h1 class="mb-4">Dashboard</h1>
    <p class="text-muted">Welcome to the Student Course Management System.</p>

    <div v-if="loading" class="alert alert-info">
      Loading dashboard...
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="row g-3">
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h2 class="h5">Available Courses</h2>
            <p class="display-6 mb-3">{{ courseCount }}</p>
            <RouterLink to="/courses" class="btn btn-primary">
              {{ authStore.user?.role === 'admin' ? 'Manage Courses' : 'Browse Courses' }}
            </RouterLink>
          </div>
        </div>
      </div>

      <div v-if="authStore.user?.role === 'student'" class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h2 class="h5">My Enrollments</h2>
            <p class="display-6 mb-3">{{ enrollmentCount }}</p>
            <RouterLink to="/enrollments" class="btn btn-primary">
              View Enrollments
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'

const courseCount = ref<number | null>(null)
const enrollmentCount = ref<number | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const [coursesResponse, enrollmentsResponse] = await Promise.all([
      api.get('/courses'),
      api.get('/enrollments'),
    ])

    const courses = coursesResponse.data.data
    const enrollments = enrollmentsResponse.data.data

    courseCount.value = Array.isArray(courses) ? courses.length : 0
    enrollmentCount.value = Array.isArray(enrollments)
      ? enrollments.length
      : 0
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
              Browse Courses
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="col-md-6">
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


<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'

interface Course {
  id: string
  title: string
  description: string | null
  instructor_name: string
  duration_hours: number
}

const courses = ref<Course[]>([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const enrollingId = ref<number | string | null>(null)

onMounted(loadCourses)

async function loadCourses() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/courses')
    courses.value = response.data.data
  } catch {
    error.value = 'Unable to load courses.'
  } finally {
    loading.value = false
  }
}

async function enroll(courseId: number | string) {
  enrollingId.value = courseId
  error.value = ''
  success.value = ''

  try {
    await api.post(`/enrollments/${courseId}`)
    success.value = 'Enrollment successful.'
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ?? 'Unable to enroll in this course.'
  } finally {
    enrollingId.value = null
  }
}
</script>

<template>
  <main class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Courses</h1>
      <RouterLink to="/dashboard" class="btn btn-outline-secondary">
        Dashboard
      </RouterLink>
    </div>

    <div v-if="success" class="alert alert-success">{{ success }}</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="loading" class="alert alert-info">Loading courses...</div>

    <div v-else-if="!error && courses.length === 0" class="alert alert-secondary">
      No courses are available.
    </div>

    <div v-else class="row g-3">
      <div v-for="course in courses" :key="course.id" class="col-md-6 col-lg-4">
        <article class="card h-100">
          <div class="card-body">
            <h2 class="h5">{{ course.title }}</h2>
            <p class="text-muted">
              {{ course.description || 'No description available.' }}
            </p>
            <button
              class="btn btn-primary"
              :disabled="enrollingId !== null"
              @click="enroll(course.id)"
            >
              {{ enrollingId === course.id ? 'Enrolling...' : 'Enroll' }}
            </button>
          </div>
        </article>
      </div>
    </div>
  </main>
</template>

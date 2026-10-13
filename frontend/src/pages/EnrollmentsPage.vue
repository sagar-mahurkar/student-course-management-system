
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../services/api'

interface Enrollment {
  id: string
  user_id: string
  course_id: string
  enrolled_at: string
}

const enrollments = ref<Enrollment[]>([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const unenrollingId = ref<number | string | null>(null)

onMounted(loadEnrollments)

async function loadEnrollments() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/enrollments')
    enrollments.value = response.data.data
  } catch {
    error.value = 'Unable to load your enrollments.'
  } finally {
    loading.value = false
  }
}

async function unenroll(enrollmentId: number | string) {
  unenrollingId.value = enrollmentId
  error.value = ''
  success.value = ''

  try {
    await api.delete(`/enrollments/${enrollmentId}`)
    enrollments.value = enrollments.value.filter(
      (enrollment) => enrollment.id !== enrollmentId,
    )
    success.value = 'You have unenrolled successfully.'
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ?? 'Unable to unenroll.'
  } finally {
    unenrollingId.value = null
  }
}
</script>

<template>
  <main class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>My Enrollments</h1>
      <RouterLink to="/courses" class="btn btn-primary">
        Browse Courses
      </RouterLink>
    </div>

    <div v-if="success" class="alert alert-success">{{ success }}</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="loading" class="alert alert-info">
      Loading enrollments...
    </div>

    <div v-else-if="enrollments.length === 0" class="alert alert-secondary">
      You are not enrolled in any courses.
    </div>

    <div v-else class="list-group">
      <div
        v-for="enrollment in enrollments"
        :key="enrollment.id"
        class="list-group-item d-flex justify-content-between align-items-center gap-3"
      >
        <div>
          <h2 class="h6 mb-1">Course ID: {{ enrollment.course_id }}</h2>
          <small class="text-muted">
            Enrollment ID: {{ enrollment.id }}
          </small>
        </div>

        <button
          class="btn btn-outline-danger btn-sm"
          :disabled="unenrollingId !== null"
          @click="unenroll(enrollment.id)"
        >
          {{ unenrollingId === enrollment.id ? 'Removing...' : 'Unenroll' }}
        </button>
      </div>
    </div>
  </main>
</template>

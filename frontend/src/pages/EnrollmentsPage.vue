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
const unenrollingId = ref<string | null>(null)

onMounted(loadEnrollments)

async function loadEnrollments() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get<{ data: Enrollment[] }>('/enrollments')
    enrollments.value = response.data.data
  } catch (err: unknown) {
    error.value = getErrorMessage(err, 'Unable to load your enrollments.')
  } finally {
    loading.value = false
  }
}

async function unenroll(enrollmentId: string) {
  unenrollingId.value = enrollmentId
  error.value = ''
  success.value = ''

  try {
    await api.delete(`/enrollments/${enrollmentId}`)
    enrollments.value = enrollments.value.filter(
      (enrollment) => enrollment.id !== enrollmentId,
    )
    success.value = 'You have unenrolled successfully.'
  } catch (err: unknown) {
    error.value = getErrorMessage(err, 'Unable to unenroll from this course.')
  } finally {
    unenrollingId.value = null
  }
}

function formatDate(value: string): string {
  if (!value) return 'Date unavailable'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'Date unavailable'

  return new Intl.DateTimeFormat(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date)
}

function getErrorMessage(err: unknown, fallback: string): string {
  if (
    typeof err === 'object' &&
    err !== null &&
    'response' in err &&
    typeof err.response === 'object' &&
    err.response !== null &&
    'data' in err.response &&
    typeof err.response.data === 'object' &&
    err.response.data !== null &&
    'error' in err.response.data &&
    typeof err.response.data.error === 'object' &&
    err.response.data.error !== null &&
    'message' in err.response.data.error &&
    typeof err.response.data.error.message === 'string'
  ) {
    return err.response.data.error.message
  }

  return fallback
}
</script>

<template>
  <main class="container py-4">
    <header class="enrollments-header">
      <div>
        <h1 class="mb-1">My Enrollments</h1>
        <p class="text-muted mb-0">
          Keep track of the courses you are taking.
        </p>
      </div>

      <RouterLink
        v-if="enrollments.length > 0"
        to="/courses"
        class="btn btn-primary"
      >
        Browse Courses
      </RouterLink>
    </header>

    <div v-if="success" class="alert alert-success" role="status">
      {{ success }}
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
      <button
        v-if="enrollments.length === 0 && !loading"
        class="btn btn-sm btn-outline-danger ms-2"
        type="button"
        @click="loadEnrollments"
      >
        Try again
      </button>
    </div>

    <div v-if="loading" class="status-panel" role="status">
      <span class="spinner-border text-primary" aria-hidden="true"></span>
      <p class="mb-0 mt-3 text-muted">Loading your enrollments...</p>
    </div>

    <section
      v-else-if="!error && enrollments.length === 0"
      class="empty-state"
      aria-labelledby="empty-enrollments-title"
    >
      <div class="empty-state-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none">
          <path
            d="M5 4.75A1.75 1.75 0 0 1 6.75 3h10.5A1.75 1.75 0 0 1 19 4.75v14.5A1.75 1.75 0 0 1 17.25 21H6.75A1.75 1.75 0 0 1 5 19.25V4.75Z"
            stroke="currentColor"
            stroke-width="1.6"
          />
          <path
            d="M8 8h8M8 12h8M8 16h5"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linecap="round"
          />
        </svg>
      </div>
      <h2 id="empty-enrollments-title" class="h5">No enrollments yet</h2>
      <p class="text-muted empty-state-copy">
        Once you enroll in a course, it will appear here.
      </p>
      <RouterLink to="/courses" class="btn btn-primary">
        Explore Courses
      </RouterLink>
    </section>

    <section v-else-if="enrollments.length > 0" class="enrollment-list">
      <article
        v-for="enrollment in enrollments"
        :key="enrollment.id"
        class="enrollment-card"
      >
        <div class="enrollment-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none">
            <path
              d="M4 5.75A1.75 1.75 0 0 1 5.75 4h12.5A1.75 1.75 0 0 1 20 5.75v12.5A1.75 1.75 0 0 1 18.25 20H5.75A1.75 1.75 0 0 1 4 18.25V5.75Z"
              stroke="currentColor"
              stroke-width="1.6"
            />
            <path
              d="M8 8h8M8 12h8M8 16h4"
              stroke="currentColor"
              stroke-width="1.6"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <div class="enrollment-details">
          <h2 class="h6 mb-1">Course #{{ enrollment.course_id }}</h2>
          <p class="enrollment-date mb-1">
            Enrolled {{ formatDate(enrollment.enrolled_at) }}
          </p>
          <span class="enrollment-reference">
            Enrollment #{{ enrollment.id }}
          </span>
        </div>

        <button
          class="btn btn-outline-danger unenroll-button"
          type="button"
          :disabled="unenrollingId !== null"
          @click="unenroll(enrollment.id)"
        >
          <span
            v-if="unenrollingId === enrollment.id"
            class="spinner-border spinner-border-sm me-1"
            aria-hidden="true"
          ></span>
          {{ unenrollingId === enrollment.id ? 'Removing...' : 'Unenroll' }}
        </button>
      </article>
    </section>
  </main>
</template>

<style scoped>
.enrollments-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.empty-state,
.status-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 14rem;
  padding: 2.5rem 1.5rem;
  text-align: center;
  border: 1px dashed var(--bs-border-color, #dee2e6);
  border-radius: 0.75rem;
  background: var(--bs-tertiary-bg, #f8f9fa);
}

.empty-state-icon,
.enrollment-icon {
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: var(--bs-primary, #0d6efd);
  background: var(--bs-primary-bg-subtle, #cfe2ff);
}

.empty-state-icon {
  width: 3.25rem;
  height: 3.25rem;
  margin-bottom: 1rem;
  border-radius: 50%;
}

.empty-state-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.empty-state-copy {
  max-width: 26rem;
  margin-bottom: 1.25rem;
}

.enrollment-list {
  display: grid;
  gap: 1rem;
}

.enrollment-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  border: 1px solid var(--bs-border-color, #dee2e6);
  border-radius: 0.75rem;
  background: var(--bs-body-bg, #fff);
  transition: box-shadow 150ms ease, border-color 150ms ease;
}

.enrollment-card:hover {
  border-color: var(--bs-primary-border-subtle, #9ec5fe);
  box-shadow: 0 0.4rem 1.1rem rgb(33 37 41 / 6%);
}

.enrollment-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 0.7rem;
}

.enrollment-icon svg {
  width: 1.4rem;
  height: 1.4rem;
}

.enrollment-details {
  min-width: 0;
  flex: 1;
}

.enrollment-date {
  color: var(--bs-secondary-color, #6c757d);
  font-size: 0.9rem;
}

.enrollment-reference {
  color: var(--bs-secondary-color, #6c757d);
  font-size: 0.78rem;
}

.unenroll-button {
  flex: 0 0 auto;
}

@media (max-width: 576px) {
  .enrollments-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .enrollments-header h1 {
    font-size: 1.75rem;
  }

  .enrollment-card {
    align-items: flex-start;
    flex-wrap: wrap;
    padding: 1rem;
  }

  .enrollment-details {
    flex-basis: calc(100% - 4rem);
  }

  .unenroll-button {
    margin-left: 4rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .enrollment-card {
    transition: none;
  }
}
</style>

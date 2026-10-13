<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

interface Course {
  id: string
  title: string
  description: string
  instructor_name: string
  duration_hours: number
}

interface Enrollment {
  id: string
  course_id: string
  enrolled_at: string
}

interface CreateCoursePayload {
  title: string
  description: string
  instructor_name: string
  duration_hours: number
}

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.user?.role === 'admin')
const isStudent = computed(() => authStore.user?.role === 'student')

const courses = ref<Course[]>([])
const enrolledCourseIds = ref<Set<string>>(new Set())
const loading = ref(true)
const loadingEnrollments = ref(false)
const pageError = ref('')
const enrollmentError = ref('')
const formError = ref('')
const formSuccess = ref('')
const enrollingId = ref<string | null>(null)
const creating = ref(false)
const showCreateModal = ref(false)

const form = reactive<CreateCoursePayload>({
  title: '',
  description: '',
  instructor_name: '',
  duration_hours: 1,
})

onMounted(() => {
  void initializePage()
})

async function initializePage() {
  await Promise.all([loadCourses(), ...(isStudent.value ? [loadStudentEnrollments()] : [])])
}

async function loadCourses() {
  loading.value = true
  pageError.value = ''

  try {
    const response = await api.get<{ data: Course[] }>('/courses')
    courses.value = response.data.data
  } catch (err: unknown) {
    pageError.value = getErrorMessage(err, 'Unable to load courses.')
  } finally {
    loading.value = false
  }
}

async function loadStudentEnrollments() {
  loadingEnrollments.value = true
  enrollmentError.value = ''

  try {
    const response = await api.get<{ data: Enrollment[] }>('/enrollments')
    enrolledCourseIds.value = new Set(
      response.data.data.map((enrollment) => enrollment.course_id),
    )
  } catch (err: unknown) {
    enrollmentError.value = getErrorMessage(
      err,
      'Unable to check your current enrollments. Refresh the page to try again.',
    )
  } finally {
    loadingEnrollments.value = false
  }
}

function openCreateModal() {
  formError.value = ''
  formSuccess.value = ''
  showCreateModal.value = true
}

function closeCreateModal() {
  if (creating.value) return
  showCreateModal.value = false
  formError.value = ''
}

async function createCourse() {
  creating.value = true
  formError.value = ''
  formSuccess.value = ''

  const payload: CreateCoursePayload = {
    title: form.title.trim(),
    description: form.description.trim(),
    instructor_name: form.instructor_name.trim(),
    duration_hours: Number(form.duration_hours),
  }

  try {
    await api.post('/courses', payload)
    Object.assign(form, {
      title: '',
      description: '',
      instructor_name: '',
      duration_hours: 1,
    })
    showCreateModal.value = false
    formSuccess.value = 'Course created successfully.'
    await loadCourses()
  } catch (err: unknown) {
    formError.value = getErrorMessage(err, 'Unable to create course.')
  } finally {
    creating.value = false
  }
}

async function enroll(courseId: string) {
  if (enrolledCourseIds.value.has(courseId) || enrollingId.value !== null) {
    return
  }

  enrollingId.value = courseId
  pageError.value = ''
  enrollmentError.value = ''
  formSuccess.value = ''

  try {
    await api.post(`/enrollments/${courseId}`)
    enrolledCourseIds.value = new Set([...enrolledCourseIds.value, courseId])
    formSuccess.value = 'Enrollment successful.'

    // Reconcile with the server's enrollment list when possible.
    try {
      await loadStudentEnrollments()
    } catch {
      // The successful enrollment is already reflected locally.
    }
  } catch (err: unknown) {
    pageError.value = getErrorMessage(err, 'Unable to enroll in this course.')
  } finally {
    enrollingId.value = null
  }
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
    <header class="courses-header">
      <div>
        <h1 class="mb-1">Courses</h1>
        <p class="text-muted mb-0">Explore and manage the course catalog.</p>
      </div>

      <button
        v-if="isAdmin"
        class="btn btn-primary"
        type="button"
        @click="openCreateModal"
      >
        <span class="button-plus" aria-hidden="true">+</span>
        Create Course
      </button>
    </header>

    <div v-if="formSuccess" class="alert alert-success" role="status">
      {{ formSuccess }}
    </div>
    <div v-if="pageError" class="alert alert-danger" role="alert">
      {{ pageError }}
    </div>
    <div v-if="enrollmentError" class="alert alert-warning" role="alert">
      {{ enrollmentError }}
      <button
        class="btn btn-sm btn-outline-warning ms-2"
        type="button"
        :disabled="loadingEnrollments"
        @click="loadStudentEnrollments"
      >
        {{ loadingEnrollments ? 'Checking...' : 'Retry' }}
      </button>
    </div>

    <div v-if="loading" class="alert alert-info" role="status">
      Loading courses...
    </div>

    <div v-else-if="!pageError && courses.length === 0" class="empty-state">
      <div class="empty-state-icon" aria-hidden="true">▤</div>
      <h2 class="h5">No courses yet</h2>
      <p class="text-muted mb-0">
        {{ isAdmin ? 'Create your first course to get started.' : 'Please check back later for available courses.' }}
      </p>
    </div>

    <div v-else-if="courses.length > 0" class="row g-3">
      <div v-for="course in courses" :key="course.id" class="col-md-6 col-lg-4">
        <article class="card course-card h-100">
          <div class="card-body">
            <h2 class="h5">{{ course.title }}</h2>
            <p class="course-description">
              {{ course.description || 'No description available.' }}
            </p>
            <div class="course-meta">
              <p><strong>Instructor</strong><span>{{ course.instructor_name }}</span></p>
              <p><strong>Duration</strong><span>{{ course.duration_hours }} hours</span></p>
            </div>

            <span
              v-if="isStudent && enrolledCourseIds.has(course.id)"
              class="badge text-bg-success mt-2"
            >
              Enrolled
            </span>
            <button
              v-else-if="isStudent"
              class="btn btn-primary mt-2"
              :disabled="enrollingId !== null || loadingEnrollments"
              @click="enroll(course.id)"
            >
              {{
                enrollingId === course.id
                  ? 'Enrolling...'
                  : loadingEnrollments
                    ? 'Checking enrollment...'
                    : 'Enroll'
              }}
            </button>
          </div>
        </article>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="showCreateModal && isAdmin"
        class="modal-backdrop-custom"
        @click.self="closeCreateModal"
      >
        <section
          class="course-modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="create-course-title"
          aria-describedby="create-course-description"
        >
          <header class="course-modal-header">
            <div>
              <p class="modal-eyebrow mb-1">COURSE CATALOG</p>
              <h2 id="create-course-title" class="course-modal-title">Create course</h2>
              <p id="create-course-description" class="modal-subtitle mb-0">
                Add a new course for students to discover.
              </p>
            </div>
            <button
              class="modal-close"
              type="button"
              aria-label="Close dialog"
              :disabled="creating"
              @click="closeCreateModal"
            >
              &times;
            </button>
          </header>

          <form @submit.prevent="createCourse">
            <div class="course-modal-body">
              <div v-if="formError" class="alert alert-danger" role="alert">
                {{ formError }}
              </div>

              <div class="mb-3">
                <label for="course-title" class="form-label">Course title <span class="required-mark">*</span></label>
                <input
                  id="course-title"
                  v-model="form.title"
                  class="form-control modal-input"
                  type="text"
                  maxlength="150"
                  placeholder="e.g. Introduction to Python"
                  autocomplete="off"
                  required
                  :disabled="creating"
                />
              </div>

              <div class="mb-3">
                <label for="course-description" class="form-label">Description <span class="required-mark">*</span></label>
                <textarea
                  id="course-description"
                  v-model="form.description"
                  class="form-control modal-input"
                  rows="3"
                  placeholder="What will students learn in this course?"
                  required
                  :disabled="creating"
                ></textarea>
              </div>

              <div class="mb-3">
                <label for="course-instructor" class="form-label">Instructor name <span class="required-mark">*</span></label>
                <input
                  id="course-instructor"
                  v-model="form.instructor_name"
                  class="form-control modal-input"
                  type="text"
                  maxlength="100"
                  placeholder="e.g. Priya Sharma"
                  autocomplete="off"
                  required
                  :disabled="creating"
                />
              </div>

              <div>
                <label for="course-duration" class="form-label">Duration <span class="required-mark">*</span></label>
                <div class="duration-field">
                  <input
                    id="course-duration"
                    v-model.number="form.duration_hours"
                    class="form-control modal-input"
                    type="number"
                    min="1"
                    step="1"
                    required
                    :disabled="creating"
                  />
                  <span class="duration-suffix">hours</span>
                </div>
              </div>
            </div>

            <footer class="course-modal-footer">
              <button
                class="btn btn-outline-secondary"
                type="button"
                :disabled="creating"
                @click="closeCreateModal"
              >
                Cancel
              </button>
              <button class="btn btn-primary" type="submit" :disabled="creating">
                <span v-if="creating" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                {{ creating ? 'Creating course...' : 'Create course' }}
              </button>
            </footer>
          </form>
        </section>
      </div>
    </Teleport>
  </main>
</template>

<style scoped>
.courses-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.button-plus {
  margin-right: 0.35rem;
  font-size: 1.2rem;
  line-height: 1;
  vertical-align: -1px;
}

.empty-state {
  padding: 3rem 1.5rem;
  text-align: center;
  border: 1px dashed var(--bs-border-color, #dee2e6);
  border-radius: 0.75rem;
  background: var(--bs-tertiary-bg, #f8f9fa);
}

.empty-state-icon {
  display: grid;
  place-items: center;
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem;
  border-radius: 50%;
  color: var(--bs-primary, #0d6efd);
  background: var(--bs-primary-bg-subtle, #cfe2ff);
  font-size: 1.5rem;
}

.course-card {
  border-color: var(--bs-border-color, #dee2e6);
  border-radius: 0.75rem;
  transition: box-shadow 150ms ease, transform 150ms ease;
}

.course-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1.25rem rgb(33 37 41 / 8%);
}

.course-description {
  min-height: 3rem;
  color: var(--bs-secondary-color, #6c757d);
  white-space: pre-line;
}

.course-meta {
  display: grid;
  gap: 0.65rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--bs-border-color, #dee2e6);
}

.course-meta p {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin: 0;
  font-size: 0.9rem;
}

.course-meta p span {
  text-align: right;
}

.modal-backdrop-custom {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
  padding: 1.25rem;
  background: rgb(15 23 42 / 58%);
  backdrop-filter: blur(3px);
}

.course-modal {
  width: 100%;
  max-width: 560px;
  max-height: min(90vh, 800px);
  overflow-y: auto;
  background: var(--bs-body-bg, #fff);
  color: var(--bs-body-color, #212529);
  border: 1px solid rgb(255 255 255 / 55%);
  border-radius: 1rem;
  box-shadow: 0 1.5rem 4rem rgb(0 0 0 / 24%);
  animation: modal-enter 160ms ease-out;
}

.course-modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 1px solid var(--bs-border-color, #dee2e6);
}

.modal-eyebrow {
  color: var(--bs-primary, #0d6efd);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.09em;
}

.course-modal-title {
  margin: 0;
  font-size: 1.45rem;
  font-weight: 650;
  letter-spacing: -0.025em;
}

.modal-subtitle {
  margin-top: 0.4rem;
  color: var(--bs-secondary-color, #6c757d);
  font-size: 0.9rem;
}

.modal-close {
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  width: 2.25rem;
  height: 2.25rem;
  padding: 0;
  border: 0;
  border-radius: 0.5rem;
  color: var(--bs-secondary-color, #6c757d);
  background: transparent;
  font-size: 1.8rem;
  line-height: 1;
}

.modal-close:hover:not(:disabled) {
  color: var(--bs-body-color, #212529);
  background: var(--bs-tertiary-bg, #f8f9fa);
}

.course-modal-body {
  padding: 1.5rem;
}

.course-modal-body .form-label {
  margin-bottom: 0.45rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.required-mark {
  color: var(--bs-danger, #dc3545);
}

.modal-input {
  min-height: 2.75rem;
  padding: 0.65rem 0.8rem;
  border-radius: 0.55rem;
  background-color: var(--bs-body-bg, #fff);
}

textarea.modal-input {
  min-height: 6.5rem;
  resize: vertical;
}

.modal-input:focus {
  border-color: var(--bs-primary, #0d6efd);
  box-shadow: 0 0 0 0.2rem rgb(13 110 253 / 14%);
}

.duration-field {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.duration-suffix {
  color: var(--bs-secondary-color, #6c757d);
  font-size: 0.9rem;
}

.course-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.65rem;
  padding: 1rem 1.5rem 1.25rem;
  border-top: 1px solid var(--bs-border-color, #dee2e6);
  background: var(--bs-tertiary-bg, #f8f9fa);
  border-radius: 0 0 1rem 1rem;
}

.course-modal-footer .btn {
  min-height: 2.65rem;
  padding-inline: 1rem;
  border-radius: 0.55rem;
}

@keyframes modal-enter {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.99);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 576px) {
  .courses-header {
    align-items: flex-start;
  }

  .courses-header h1 {
    font-size: 1.75rem;
  }

  .modal-backdrop-custom {
    align-items: flex-start;
    padding: 0.75rem;
  }

  .course-modal {
    max-height: calc(100vh - 1.5rem);
    margin-block: auto;
    border-radius: 0.8rem;
  }

  .course-modal-header,
  .course-modal-body {
    padding: 1.1rem;
  }

  .course-modal-footer {
    padding: 0.9rem 1.1rem 1.1rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .course-modal,
  .course-card {
    animation: none;
    transition: none;
  }
}
</style>

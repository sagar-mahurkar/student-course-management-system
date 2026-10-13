import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from 'vue-router'

import AppLayout from '../layouts/AppLayout.vue'
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import CoursesPage from '../pages/CoursesPage.vue'
import EnrollmentsPage from '../pages/EnrollmentsPage.vue'
import { useAuthStore } from '../stores/auth'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    guestOnly?: boolean
    role?: 'student' | 'admin'
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
    meta: { guestOnly: true },
  },
  {
    path: '/',
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: { name: 'dashboard' },
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardPage,
      },
      {
        path: 'courses',
        name: 'courses',
        component: CoursesPage,
      },
      {
        path: 'enrollments',
        name: 'enrollments',
        component: EnrollmentsPage,
        meta: { role: 'student' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  await authStore.initializeAuth()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }

  if (to.meta.role && authStore.user?.role !== to.meta.role) {
    return { name: 'dashboard' }
  }

  return true
})

export default router

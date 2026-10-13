
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import CoursesPage from '../pages/CoursesPage.vue'
import EnrollmentsPage from '../pages/EnrollmentsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: LoginPage },
    { path: '/register', name: 'register', component: RegisterPage },
    { path: '/dashboard', name: 'dashboard', component: DashboardPage },
    { path: '/courses', name: 'courses', component: CoursesPage },
    {
      path: '/enrollments',
      name: 'enrollments',
      component: EnrollmentsPage,
    },
    { path: '/', redirect: '/dashboard' },
  ],
})

export default router

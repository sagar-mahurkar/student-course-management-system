<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = () => {
  authStore.logout();
  router.push("/login");
};
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-light border-bottom">
    <div class="container">
      <RouterLink to="/" class="navbar-brand fw-semibold">
        Expense Tracker
      </RouterLink>

      <div class="navbar-nav me-auto">
        <RouterLink to="/" class="nav-link">Dashboard</RouterLink>

        <RouterLink to="/transactions" class="nav-link">
          Transactions
        </RouterLink>

        <RouterLink to="/categories" class="nav-link">
          Categories
        </RouterLink>
      </div>

      <div class="d-flex align-items-center gap-3">
        <span class="text-dark">
          {{ authStore.user?.full_name }}
        </span>

        <button
          type="button"
          class="btn btn-outline-secondary btn-sm"
          @click="handleLogout"
        >
          Logout
        </button>
      </div>
    </div>
  </nav>

  <main>
    <RouterView />
  </main>
</template>

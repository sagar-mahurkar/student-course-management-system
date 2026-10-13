<script setup lang="ts">
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const handleSubmit = async () => {
  errorMessage.value = "";
  isLoading.value = true;

  try {
    await authStore.login(email.value, password.value);
    await router.push("/");
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.error?.message ||
      "Unable to login. Please try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-5" style="width: 500px">
      <h1 class="mb-4 text-center">Login</h1>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-control"
            required
            autocomplete="email"
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-control"
            required
            autocomplete="current-password"
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="isLoading"
        >
          {{ isLoading ? "Logging in..." : "Login" }}
        </button>
      </form>

      <div class="mt-4 text-center">
        Don't have an account?
        <RouterLink to="/register">Register</RouterLink>
      </div>
    </div>
  </div>
</template>

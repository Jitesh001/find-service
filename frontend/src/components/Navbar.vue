<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="logo">FindService</router-link>
      <ul class="nav-links">
        <!-- Links for logged-out users -->
        <li v-if="!isLoggedIn">
          <router-link to="/">Home</router-link>
        </li>
        <li v-if="!isLoggedIn">
          <router-link to="/login">Login</router-link>
        </li>
        <li v-if="!isLoggedIn">
          <router-link to="/signup/customer">Customer Sign Up</router-link>
        </li>
        <li v-if="!isLoggedIn">
          <router-link to="/signup/service">Service Sign Up</router-link>
        </li>

        <!-- Links for logged-in users -->
        <li v-if="isLoggedIn">
          <router-link to="/">Home</router-link>
        </li>
        <li v-if="isLoggedIn">
          <button @click="logout" class="logout-button">Logout</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { authState, setAuthState } from "@/store/auth"; // Assuming authState is in the store
import { useRouter } from "vue-router";
import { toRefs } from "vue";
import { stopLocationUpdates } from "@/utils/locationUpdater"; // Assuming location updater utils

// Setup the router
const router = useRouter();

// Destructure the reactive authState to get isLoggedIn
const { isLoggedIn } = toRefs(authState);

// Logout function to handle sign-out process
const logout = () => {
  localStorage.removeItem("authToken");
  setAuthState(false);
  router.push("/login");
  stopLocationUpdates();
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #4caf50;
  color: white;
}

.navbar .logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.navbar .nav-links {
  list-style: none;
  display: flex;
  gap: 1rem;
}

.navbar .nav-links a {
  text-decoration: none;
  color: white;
}

.navbar .logout-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1rem;
  text-decoration: underline;
  padding: 0;
}

.navbar .logout-button:hover {
  text-decoration: none;
}
</style>

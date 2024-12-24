<template>
  <div class="home-page">
    <h1>Welcome to FindService!</h1>
    <p>Discover and connect with service providers or customers near you.</p>
    <div class="buttons">
      <router-link v-if="!isLoggedIn" to="/signup/customer" class="btn"
        >Sign Up as Customer</router-link
      >
      <router-link v-if="!isLoggedIn" to="/signup/service" class="btn"
        >Sign Up as Service Provider</router-link
      >
      <router-link v-if="!isLoggedIn" to="/login" class="btn"
        >Login</router-link
      >
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const isLoggedIn = ref(false);

// Check if the user is logged in when the component is mounted
onMounted(() => {
  const token = localStorage.getItem("authToken");
  isLoggedIn.value = !!token; // Set isLoggedIn based on the presence of the token
});
</script>

<style scoped>
.home-page {
  text-align: center;
  padding: 2rem;
}
.home-page .btn {
  margin: 1rem;
  padding: 1rem 2rem;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
</style>

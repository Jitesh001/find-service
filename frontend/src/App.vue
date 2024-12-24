<template>
  <div id="app-design">
    <Navbar />
    <RouterView />
  </div>
</template>

<script setup>
import {
  startLocationUpdates,
  stopLocationUpdates,
} from "@/utils/locationUpdater";
import Navbar from "./components/Navbar.vue";
import { authState } from "@/store/auth";
import { ref, onMounted } from "vue";


onMounted() {
    // Initialize auth state based on localStorage
    const token = localStorage.getItem("authToken");
    authState.isLoggedIn = !!token;
  },
</script>

<style>
/* Basic styles for layout */
#app-design {
  font-family: Arial, sans-serif;
  text-align: center;
  color: #333;
}
</style>

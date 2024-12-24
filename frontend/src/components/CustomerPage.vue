<template>
  <div class="customer-page">
    <h1>Welcome, Customer!</h1>
    <p>Your current location is being tracked.</p>
    <p>Here are some sample services available near you:</p>
    <ul>
      <li v-for="service in services" :key="service.id">
        {{ service.service_name }} - Located at ({{ service.latitude }},
        {{ service.longitude }})
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { post, get } from "@/utils/api";

// Reactive state to hold the services data
const services = ref([]);

// Fetch the services data when the component is mounted
onMounted(async () => {
  try {
    const response = await get("/api/services/");
    services.value = response.data;
  } catch (error) {
    console.error("Failed to fetch services:", error);
  }
});
</script>

<style scoped>
.customer-page {
  text-align: center;
  padding: 2rem;
}

.customer-page ul {
  list-style: none;
  padding: 0;
}

.customer-page li {
  background-color: #f9f9f9;
  margin: 0.5rem 0;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>

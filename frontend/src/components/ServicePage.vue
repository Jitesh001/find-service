<template>
  <div class="service-page">
    <h1>Welcome, Service Provider!</h1>
    <p>Your current location is being tracked.</p>
    <p>Here are some nearby customers:</p>
    <ul>
      <li v-for="customer in customers" :key="customer.id">
        {{ customer.user.full_name }} - Located at ({{ customer.latitude }},
        {{ customer.longitude }})
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { post, get } from "@/utils/api";

// Reactive state to hold the customers data
const customers = ref([]);

// Fetch the customers data when the component is mounted
onMounted(async () => {
  try {
    const response = await get("/api/customers/");
    customers.value = response.data;
  } catch (error) {
    console.error("Failed to fetch customers:", error);
  }
});
</script>

<style scoped>
.service-page {
  text-align: center;
  padding: 2rem;
}

.service-page ul {
  list-style: none;
  padding: 0;
}

.service-page li {
  background-color: #f9f9f9;
  margin: 0.5rem 0;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>

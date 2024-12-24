<template>
  <form @submit.prevent="login">
    <input v-model="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { setAuthState } from "@/store/auth";
import { startLocationUpdates } from "@/utils/locationUpdater";
import { post, get } from "@/utils/api"; // Custom functions to replace axios

// Router instance
const router = useRouter();

// Reactive states
const email = ref("");
const password = ref("");
const errorMessage = ref(null);

// Request location access from user
const requestLocationAccess = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject("Geolocation is not supported by this browser.");
    }

    navigator.geolocation.getCurrentPosition(
      (position) => resolve(position),
      (error) => reject(error.message)
    );
  });
};

// Login function
const login = async () => {
  try {
    errorMessage.value = null; // Reset error message

    // Get CSRF token from cookies
    let csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];

    if (!csrfToken) {
      console.warn("CSRF token not found. Fetching from backend...");
      await fetchCsrfToken(); // Fetch token if missing
      csrfToken = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1];
    }

    // Perform login request
    const { status, data } = await post(
      "/api/login/",
      {
        email: email.value,
        password: password.value,
      },
      {
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
    );

    if (status === 200) {
      localStorage.setItem("authToken", data.token); // Store auth token
      setAuthState(true); // Update auth state

      // Try to request location access
      try {
        await requestLocationAccess();
        console.log("Location access granted.");
        startLocationUpdates(); // Start location updates

        // Redirect based on user type
        const redirectUrl =
          data.user_type === "customer" ? "/customer-page" : "/service-page";
        router.push(redirectUrl);
      } catch (locationError) {
        console.error(
          "Location access denied or error occurred:",
          locationError
        );
        alert(
          "Location access is required to use this application. Logging out."
        );
        logout();
      }
    } else {
      errorMessage.value = data.message || "Login failed. Please try again.";
    }
  } catch (error) {
    console.error("Login failed:", error.response?.data || error);
    errorMessage.value = "Login failed. Please check your credentials.";
  }
};

// Fetch CSRF token
const fetchCsrfToken = async () => {
  try {
    const { status, data } = await get("/api/csrf-token/");
    if (status === 200) {
      const csrfToken = data.csrfToken;
      document.cookie = `csrftoken=${csrfToken}; path=/;`; // Store CSRF token
      console.log("CSRF token fetched and stored.");
    } else {
      throw new Error("Failed to fetch CSRF token");
    }
  } catch (error) {
    console.error("Failed to fetch CSRF token:", error);
    alert("Unable to fetch CSRF token. Please try again.");
  }
};

// Logout function
const logout = () => {
  localStorage.removeItem("authToken");
  setAuthState(false);
  router.push("/login");
};
</script>

<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}
</style>

<template>
  <form @submit.prevent="signUp">
    <h2>Service Provider Signup</h2>
    <input v-model="formData.email" type="email" placeholder="Email" required />
    <input
      v-model="formData.mobile"
      type="text"
      placeholder="Mobile Number"
      required
    />
    <input
      v-model="formData.first_name"
      type="text"
      placeholder="First Name"
      required
    />
    <input
      v-model="formData.last_name"
      type="text"
      placeholder="Last Name"
      required
    />
    <input
      v-model="formData.service_name"
      type="text"
      placeholder="Service Name"
      required
    />
    <input
      v-model="formData.password1"
      type="password"
      placeholder="Password"
      required
    />
    <input
      v-model="formData.password2"
      type="password"
      placeholder="Confirm Password"
      required
    />
    <button type="submit">Sign Up</button>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </form>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { setAuthState } from "@/store/auth";
import { post, get } from "@/utils/api";
import {
  startLocationUpdates,
  stopLocationUpdates,
} from "@/utils/locationUpdater";

// Router instance
const router = useRouter();

// Reactive form data
const formData = reactive({
  email: "",
  mobile: "",
  first_name: "",
  last_name: "",
  service_name: "",
  password1: "",
  password2: "",
});

// Error message state
const errorMessage = ref(null);

// CSRF token state
const csrfToken = ref(null);

// Sign up function
const signUp = async () => {
  try {
    errorMessage.value = null; // Reset error message

    // Ensure CSRF token is available
    if (!csrfToken.value) {
      console.warn("CSRF token not found. Fetching CSRF token...");
      await fetchCsrfToken(); // Wait for CSRF token if it's missing
    }

    // Perform signup request
    const { status, data } = await post("/api/signup/service/", formData, {
      headers: {
        "X-CSRFToken": csrfToken.value, // Send CSRF token in the header
      },
    });

    if (status === 201) {
      console.log("Signup successful:", data.message);

      // Auto-login after successful signup
      const { status: loginStatus, data: loginData } = await post(
        "/api/login/",
        {
          email: formData.email,
          password: formData.password1, // Use the password entered during signup
        },
        {
          headers: {
            "X-CSRFToken": csrfToken.value,
          },
        }
      );

      if (loginStatus === 200) {
        localStorage.setItem("authToken", loginData.token);
        setAuthState(true);
        startLocationUpdates();

        const { user_type } = loginData;
        const redirectUrl =
          user_type === "customer" ? "/customer-page" : "/service-page";
        router.push(redirectUrl);
      } else {
        errorMessage.value = loginData.message || "Failed to login.";
      }
    } else {
      errorMessage.value = data.message || "Failed to sign up.";
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = "Network error or server is down.";
  }
};

// Fetch CSRF token
const fetchCsrfToken = async () => {
  try {
    const { status, data } = await get("/api/csrf-token/");
    if (status === 200) {
      csrfToken.value = data.csrfToken;
      document.cookie = `csrftoken=${csrfToken.value}; path=/;`; // Store CSRF token in cookies
      console.log("CSRF token fetched and stored.");
    } else {
      throw new Error("Failed to fetch CSRF token");
    }
  } catch (error) {
    console.error("Failed to fetch CSRF token:", error);
    alert("Unable to fetch CSRF token. Please try again.");
  }
};

// Try to get the CSRF token from the cookie
const cookieToken = document.cookie
  .split("; ")
  .find((row) => row.startsWith("csrftoken="))
  ?.split("=")[1];

if (cookieToken) {
  csrfToken.value = cookieToken; // Set CSRF token from the cookie
}
</script>

<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}
</style>

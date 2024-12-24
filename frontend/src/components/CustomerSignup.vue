<template>
  <form @submit.prevent="signUp">
    <h2>Customer Signup</h2>
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

// Router
const router = useRouter();

// Reactive form data
const formData = reactive({
  email: "",
  mobile: "",
  first_name: "",
  last_name: "",
  password1: "",
  password2: "",
});

// Reactive state for errors
const errorMessage = ref(null);
const csrfToken = ref(null);

// Sign up function
const signUp = async () => {
  try {
    errorMessage.value = null; // Clear any previous errors

    // Ensure CSRF token is available
    if (!csrfToken.value) {
      console.warn("CSRF token not found. Fetching CSRF token...");
      await fetchCsrfToken(); // Wait until the CSRF token is fetched
    }

    // Perform signup request using custom POST method
    const { status, data } = await post("/api/signup/customer/", formData, {
      headers: {
        "X-CSRFToken": csrfToken.value,
      },
    });

    console.log("status and data as follows", status, data);

    if (status === 201) {
      console.log("Signup successful:", data.message);

      // Auto-login after successful signup
      const { status: loginStatus, data: loginData } = await post(
        "/api/login/",
        {
          email: formData.email,
          password: formData.password1,
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
      document.cookie = `csrftoken=${csrfToken.value}; path=/;`;
      console.log("CSRF token fetched and stored.");
    } else {
      throw new Error("Failed to fetch CSRF token");
    }
  } catch (error) {
    console.error("Failed to fetch CSRF token:", error);
    alert("Unable to fetch CSRF token. Please try again.");
  }
};

// Fetch CSRF token from cookies when the component is created
const cookieToken = document.cookie
  .split("; ")
  .find((row) => row.startsWith("csrftoken="))
  ?.split("=")[1];

if (cookieToken) {
  csrfToken.value = cookieToken;
}
</script>

<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}
</style>

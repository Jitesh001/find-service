import axios from "axios";

let locationUpdateInterval = null; // To store the interval ID

export function startLocationUpdates() {
  // Prevent multiple intervals
  if (locationUpdateInterval) {
    console.warn("Location updates are already running.");
    return;
  }

  // Check if the user is logged in
  const token = localStorage.getItem("authToken");

  if (!token) {
    console.warn("User is not logged in. Location updates will not start.");
    return;
  }

  if (navigator.geolocation) {
    console.log("Starting location updates...");
    locationUpdateInterval = setInterval(() => {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        try {
          const csrfToken = document.cookie
            .split("; ")
            .find((row) => row.startsWith("csrftoken="))
            ?.split("=")[1];

          if (!csrfToken) {
            console.error("CSRF token not found");
            return;
          }

          await axios.post(
            "/api/update-location/",
            { latitude, longitude },
            {
              headers: {
                "X-CSRFToken": csrfToken,
                Authorization: `Bearer ${token}`, // Include token in header if required
              },
              withCredentials: true, // Include cookies for CSRF validation
            }
          );
          console.log("Location updated successfully:", {
            latitude,
            longitude,
          });
        } catch (error) {
          console.error("Failed to update location:", error);
        }
      });
    }, 20000); // Update every 30 seconds
  } else {
    console.warn("Geolocation is not supported by this browser.");
  }
}

export function stopLocationUpdates() {
  if (locationUpdateInterval) {
    clearInterval(locationUpdateInterval);
    locationUpdateInterval = null;
    console.log("Location updates stopped.");
  } else {
    console.warn("Location updates are not running.");
  }
}

import { reactive } from "vue";

export const authState = reactive({
  isLoggedIn: false,
});

export function setAuthState(isLoggedIn) {
  authState.isLoggedIn = isLoggedIn;
}

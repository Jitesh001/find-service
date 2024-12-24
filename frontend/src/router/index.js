import { createRouter, createWebHistory } from "vue-router";
import CustomerSignup from "@/components/CustomerSignup.vue";
import ServiceSignup from "@/components/ServiceSignup.vue";
import Login from "@/components/Login.vue";
import CustomerPage from "@/components/CustomerPage.vue";
import ServicePage from "@/components/ServicePage.vue";
import Home from "@/components/Home.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/signup/customer", component: CustomerSignup },
  { path: "/signup/service", component: ServiceSignup },
  { path: "/login", component: Login },
  { path: "/customer-page", component: CustomerPage },
  { path: "/service-page", component: ServicePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

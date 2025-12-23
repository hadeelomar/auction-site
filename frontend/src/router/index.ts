import { createRouter, createWebHistory } from "vue-router"
import AuthPage from "../pages/AuthPage.vue"
import DashboardPage from "../pages/DashboardPage.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "auth",
      component: AuthPage,
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: DashboardPage,
    },
  ],
})

export default router

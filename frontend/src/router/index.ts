import { createRouter, createWebHistory } from "vue-router"
import AuthPage from "../pages/AuthPage.vue"
import DashboardPage from "../pages/DashboardPage.vue"
import { useAuthStore } from "../stores/auth"

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
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  await authStore.checkAuth()

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      next({ name: "auth" })
    } else {
      next()
    }
  } else {
    if (to.name === "auth" && authStore.isAuthenticated) {
      next({ name: "dashboard" })
    } else {
      next()
    }
  }
})

export default router

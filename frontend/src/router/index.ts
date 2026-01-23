import { createRouter, createWebHistory } from "vue-router"
import BrowseAuctionsPage from "../pages/BrowseAuctionsPage.vue"
import { useAuthStore } from "../stores/auth"

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/",
      name: "home",
      component: BrowseAuctionsPage,
    },
    {
      path: "/auction/:id",
      name: "auction-detail",
      component: () => import("../pages/AuctionDetailPage.vue"),
    },
    {
      path: "/create",
      name: "create-auction",
      component: () => import("../pages/CreateAuctionPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/edit/:id",
      name: "edit-auction",
      component: () => import("../pages/CreateAuctionPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/bids",
      name: "my-bids",
      component: () => import("../pages/MyBidsPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/auctions",
      name: "my-auctions",
      component: () => import("../pages/MyAuctionsPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("../pages/ProfilePage.vue"),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  await authStore.checkAuth()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirect to Django login page instead of Vue route
    window.location.href = "http://localhost:8001/login/"
    return false
  }
})


export default router

import { createRouter, createWebHistory } from "vue-router"
import AuthPage from "../pages/AuthPage.vue"
import DashboardPage from "../pages/DashboardPage.vue"
import { useAuthStore } from "../stores/auth"
import BrowseAuctionsPage from "../pages/BrowseAuctionsPage.vue"
import CreateAuctionPage from "../pages/CreateAuctionPage.vue"
import MyBidsPage from "../pages/MyBidsPage.vue"
import MyAuctionsPage from "../pages/MyAuctionsPage.vue"
import ProfilePage from "../pages/ProfilePage.vue"
import AuctionDetailPage from "../pages/AuctionDetailPage.vue"

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
    {
      path: "/browse",
      name: "browse-auctions",
      component: BrowseAuctionsPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/create",
      name: "create-auction",
      component: CreateAuctionPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/bids",
      name: "my-bids",
      component: MyBidsPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/auctions",
      name: "my-auctions",
      component: MyAuctionsPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfilePage,
      meta: { requiresAuth: true },
    },
    {
      path: "/auction/:id",
      name: "auction-detail",
      component: AuctionDetailPage,
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
